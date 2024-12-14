const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const fs = require('fs');

// Variáveis de controle
let qrGenerated = false;

// Função para atualizar o status do bot no arquivo
function updateStatus(status) {
    try {
        fs.writeFileSync('./status.txt', status, 'utf8');
        console.log(`Status atualizado: ${status}`);
    } catch (err) {
        console.error('Erro ao atualizar o status:', err);
    }
}

// Função para salvar o QR Code como uma imagem
function saveQRCode(qr) {
    qrcode.toFile('./qr.png', qr, (err) => {
        if (err) {
            console.error('Erro ao salvar o QR Code:', err);
        } else {
            console.log('QR Code salvo como "qr.png".');
            updateStatus('Aguardando login...');
        }
    });
}

// Função para carregar comandos do arquivo JSON
function loadCommands() {
    try {
        const data = fs.readFileSync('./config.json', 'utf8');
        return JSON.parse(data).commands || {};
    } catch (err) {
        console.error('Erro ao carregar comandos:', err);
        return {};
    }
}

// Inicialização do cliente do WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
});

// Evento de QR Code
client.on('qr', (qr) => {
    if (!qrGenerated) {
        console.log('QR Code gerado. Escaneie para logar.');
        saveQRCode(qr);
        qrGenerated = true; // Evitar múltiplos QR Codes
    }
});

// Evento quando o cliente está pronto
client.on('ready', () => {
    console.log('AstecBot está pronto para uso!');
    qrGenerated = false; // Resetar o controle
    updateStatus('Bot online e pronto para uso!');
});

// Evento quando o cliente está desconectado
client.on('disconnected', (reason) => {
    console.log(`Bot desconectado: ${reason}`);
    updateStatus('Bot desconectado. Reinicie o bot.');
});

// Evento para mensagens recebidas
client.on('message', (message) => {
    const commands = loadCommands();
    const msg = message.body.trim().toLowerCase();

    if (commands[msg]) {
        message.reply(commands[msg]);
    } else {
        console.log(`Comando não encontrado: ${msg}`);
    }
});

// Tratamento de erros de autenticação
client.on('auth_failure', (msg) => {
    console.error('Falha na autenticação:', msg);
    updateStatus('Falha na autenticação. Verifique suas credenciais.');
});

// Estado do cliente alterado
client.on('change_state', (state) => {
    console.log(`Estado do cliente alterado para: ${state}`);
    updateStatus(`Estado do cliente: ${state}`);
});

// Inicializar o cliente
try {
    client.initialize();
} catch (err) {
    console.error('Erro ao inicializar o bot:', err);
    updateStatus('Erro ao inicializar o bot.');
}
