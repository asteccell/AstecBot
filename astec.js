const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

// Lista de comandos para autoatendimento
const selfServiceCommands = {
    '/suporte': '📞 Fale com nosso suporte técnico.',
    '/faq': '❓ Veja as perguntas frequentes.',
    '/abrirchamado': '📋 Abra um chamado técnico.',
    '/statuschamado': '🔍 Consulte o status do seu chamado.',
    '/cancelarservico': '⚠️ Cancele um serviço ativo.',
};

// Lista de comandos para vendas
const salesCommands = {
    '/catalogo': '🛒 Acesse nosso catálogo.',
    '/promocoes': '🔥 Confira nossas promoções.',
    '/consultarproduto': '🔎 Detalhes sobre produtos.',
    '/orcamento': '📊 Solicite um orçamento.',
    '/contatovendas': '📞 Fale com nosso time de vendas.',
};

// Lista de respostas para saudações
const greetingResponses = {
    oi: [
        '👋 Oi! Como posso ajudar? Use */ajuda* para conhecer meus comandos.',
        '🙌 Oi! Já sabe o que fazer? Experimente */ajuda*!',
    ],
    ola: [
        '🌟 Olá! Que tal começar com */ajuda*?',
        '👋 Olá! Estou pronto para ajudar. Digite */ajuda*!',
    ],
    bom_dia: [
        '🌞 Bom dia! Espero que o seu dia seja incrível. Use */ajuda*!',
        '☕ Bom dia! Já tomou café? Aproveite e digite */ajuda*!',
    ],
    boa_tarde: [
        '🌟 Boa tarde! Como posso ajudar? Experimente */ajuda*!',
        '📋 Boa tarde! Estou aqui para ajudar. Digite */ajuda*!',
    ],
    boa_noite: [
        '🌙 Boa noite! Precisa de algo antes de descansar? Use */ajuda*!',
        '💤 Boa noite! Explore meus comandos com */ajuda*!',
    ],
};

// Inicializa o cliente WhatsApp com autenticação local
const client = new Client({
    authStrategy: new LocalAuth(),
});

// Exibe o QR Code no terminal para login
client.on('qr', (qr) => {
    console.log('QR Code recebido, escaneie com o WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// Confirmação de conexão
client.on('ready', () => {
    console.log('Bot conectado com sucesso!');
});

// Logs detalhados para mensagens recebidas
client.on('message', (message) => {
    const log = `[${new Date().toISOString()}] Mensagem de ${
        message.from
    }: ${message.body}`;
    console.log(log);

    // Salva o log em um arquivo
    fs.appendFileSync('bot_logs.txt', `${log}\n`);

    // Responde a comandos ou ignora mensagens
    handleMessage(message);
});

// Função para tratar as mensagens
function handleMessage(message) {
    const msg = message.body.toLowerCase().trim();

    // Responde às saudações
    if (['oi', '/oi'].includes(msg)) {
        message.reply(randomResponse(greetingResponses.oi));
        return;
    }
    if (['olá', 'ola', '/olá', '/ola'].includes(msg)) {
        message.reply(randomResponse(greetingResponses.ola));
        return;
    }
    if (['bom dia', '/bom dia'].includes(msg)) {
        message.reply(randomResponse(greetingResponses.bom_dia));
        return;
    }
    if (['boa tarde', '/boa tarde'].includes(msg)) {
        message.reply(randomResponse(greetingResponses.boa_tarde));
        return;
    }
    if (['boa noite', '/boa noite'].includes(msg)) {
        message.reply(randomResponse(greetingResponses.boa_noite));
        return;
    }

    // Comando de ajuda
    if (msg === '/ajuda') {
        const ajudaMessage = `
🤖 *Como usar este bot*:

📞 *Autoatendimento*:
/suporte - Fale com o suporte.
/faq - Perguntas frequentes.
/abrirchamado - Abra um chamado.
/statuschamado - Consulte o status.
/cancelarservico - Cancele um serviço.

💼 *Vendas*:
/catalogo - Veja o catálogo.
/promocoes - Promoções exclusivas.
/consultarproduto - Detalhes do produto.
/orcamento - Solicite orçamento.
/contatovendas - Fale com vendas.

✨ *Dica*: Comece com o que precisa. Estou aqui para ajudar!
        `;
        message.reply(ajudaMessage);
        return;
    }

    // Comandos de autoatendimento e vendas
    if (selfServiceCommands[msg]) {
        message.reply(selfServiceCommands[msg]);
        return;
    }
    if (salesCommands[msg]) {
        message.reply(salesCommands[msg]);
        return;
    }

    // Ignora mensagens não reconhecidas
}

// Função para pegar uma resposta aleatória
function randomResponse(responses) {
    return responses[Math.floor(Math.random() * responses.length)];
}

// Trata erros
client.on('auth_failure', (msg) => {
    console.error('Falha na autenticação:', msg);
});

client.on('disconnected', (reason) => {
    console.log('Bot desconectado:', reason);
});

// Inicializa o cliente
client.initialize();
