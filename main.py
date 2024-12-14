import json
import subprocess
import threading
import os
from tkinter import Tk, Label, Text, Button, Listbox, END, messagebox, ttk, Frame, Scrollbar
from PIL import Image, ImageTk
import time
import shutil

# Caminhos e variáveis globais
CONFIG_FILE = "config.json"
BOT_SCRIPT = "bot.js"
QR_IMAGE_PATH = "./qr.png"
STATUS_FILE = "./status.txt"
AUTH_FOLDER = "./.wwebjs_auth"
qr_code_label = None
status_label = None
bot_status = "Aguardando login..."
qr_code_visible = True

# Função para carregar comandos do arquivo JSON
def load_commands():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file).get("commands", {})
    except (FileNotFoundError, json.JSONDecodeError):
        default_data = {"commands": {}}
        save_commands(default_data)
        return default_data

# Função para salvar comandos no arquivo JSON
def save_commands(commands):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump({"commands": commands}, file, indent=4, ensure_ascii=False)

# Atualizar lista de comandos na interface
def update_command_list():
    commands = load_commands()
    command_list.delete(0, END)
    # Exibir comandos separados por "/"
    grouped_commands = {}
    for command, response in commands.items():
        grouped_commands.setdefault(response, []).append(command)
    for response, cmds in grouped_commands.items():
        command_list.insert(END, " / ".join(cmds))  # Mostrar comandos juntos separados por "/"

# Adicionar um novo comando
def add_command():
    command_input = command_entry.get().strip().lower()
    response = response_entry.get("1.0", "end-1c").strip()
    if not command_input or not response:
        messagebox.showwarning("Erro", "Preencha os campos de comando e resposta.")
        return

    commands = load_commands()
    for command in command_input.split("/"):
        commands[command.strip()] = response

    save_commands(commands)
    update_command_list()
    command_entry.delete(0, END)
    response_entry.delete("1.0", END)
    messagebox.showinfo("Sucesso", "Comando(s) adicionado(s) com sucesso!")

# Excluir um comando
def delete_command():
    selected = command_list.curselection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um comando para excluir.")
        return
    selected_item = command_list.get(selected)
    commands_to_delete = selected_item.split(" / ")  # Separar comandos agrupados
    commands = load_commands()
    for command in commands_to_delete:
        if command in commands:
            del commands[command]
    save_commands(commands)
    update_command_list()
    messagebox.showinfo("Sucesso", "Comando(s) excluído(s) com sucesso!")

# Atualizar status do bot
def update_status():
    global bot_status, qr_code_visible
    while True:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r", encoding="utf-8") as file:
                status = file.read().strip()
                if status != bot_status:
                    bot_status = status
                    status_label.config(text=f"Status: {bot_status}")
                    if "Bot online" in bot_status and qr_code_visible:
                        clear_qr_code()
                        qr_code_visible = False
        time.sleep(1)

# Exibir QR Code na interface
def display_qr_code():
    global qr_code_label, qr_code_visible
    qr_code_visible = True
    while True:
        if os.path.exists(QR_IMAGE_PATH):
            qr_image = Image.open(QR_IMAGE_PATH)
            qr_image = qr_image.resize((200, 200))
            qr_code = ImageTk.PhotoImage(qr_image)
            qr_code_label.config(image=qr_code, text="")
            qr_code_label.image = qr_code
            break
        else:
            qr_code_label.config(text="QR Code será exibido aqui", image="")
        time.sleep(1)

# Apagar o QR Code
def clear_qr_code():
    if os.path.exists(QR_IMAGE_PATH):
        os.remove(QR_IMAGE_PATH)
    qr_code_label.config(text="QR Code não disponível", image="")

# Apagar a pasta de autenticação
def clear_auth_folder():
    if os.path.exists(AUTH_FOLDER):
        try:
            shutil.rmtree(AUTH_FOLDER)
            print(f"Pasta {AUTH_FOLDER} excluída com sucesso.")
        except PermissionError:
            print("Erro: Arquivos em uso. Tentando novamente...")
            time.sleep(2)
            shutil.rmtree(AUTH_FOLDER)

# Reiniciar o bot
def restart_bot():
    global bot_status, qr_code_visible
    bot_status = "Reiniciando o bot..."
    status_label.config(text=f"Status: {bot_status}")
    clear_qr_code()
    stop_bot()  # Garantir que o bot esteja parado antes de apagar a pasta
    clear_auth_folder()  # Apagar a pasta de autenticação
    qr_code_visible = True
    start_bot()
    threading.Thread(target=display_qr_code, daemon=True).start()

# Parar o bot
def stop_bot():
    try:
        subprocess.run(["taskkill", "/IM", "node.exe", "/F"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao parar o bot: {e}")

# Iniciar o bot
def start_bot():
    def bot_process():
        try:
            print("Iniciando o AstecBot...")
            subprocess.run(["node", BOT_SCRIPT], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao iniciar o bot: {e}")
            global bot_status
            bot_status = "Erro ao iniciar o bot."
            status_label.config(text=f"Status: {bot_status}")
    threading.Thread(target=bot_process, daemon=True).start()

# Configurar estilos personalizados
def apply_custom_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TButton", font=("Arial", 12, "bold"), padding=6, background="#4CAF50", foreground="white")
    style.map("TButton", background=[("active", "#45a049")])

    style.configure("TLabel", font=("Arial", 12), padding=5)
    style.configure("TListbox", font=("Arial", 10), padding=5, background="#f9f9f9", foreground="#333")

# Configurar interface gráfica
def start_interface():
    global qr_code_label, status_label, command_entry, response_entry, command_list
    root = Tk()
    root.title("AstecBot")
    root.geometry("1000x600")
    root.configure(bg="#f4f4f4")

    # Aplicar estilos personalizados
    apply_custom_styles(root)

    header = Label(root, text="AstecBot", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10)
    header.pack(fill="x")

    status_label = Label(root, text=f"Status: {bot_status}", font=("Arial", 12), bg="#f4f4f4", fg="blue")
    status_label.pack(pady=5)

    frame_main = Frame(root, bg="#f4f4f4")
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    frame_left = Frame(frame_main, bg="#f4f4f4", relief="ridge", borderwidth=2)
    frame_left.pack(side="left", fill="both", padx=5, pady=5)

    frame_right = Frame(frame_main, bg="#f4f4f4")
    frame_right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    ttk.Label(frame_left, text="Comando (use '/' para separar):", font=("Arial", 11)).pack(anchor="w", padx=10, pady=5)
    command_entry = ttk.Entry(frame_left, font=("Arial", 10))
    command_entry.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_left, text="Resposta:", font=("Arial", 11)).pack(anchor="w", padx=10, pady=5)
    response_entry = Text(frame_left, font=("Arial", 10), height=10)
    response_entry.pack(fill="both", expand=True, padx=10, pady=5)

    button_frame = Frame(frame_left, bg="#f4f4f4")
    button_frame.pack(side="bottom", fill="x", pady=10)
    Button(button_frame, text="Adicionar Comando", command=add_command, font=("Arial", 10)).pack(side="left", padx=5)
    Button(button_frame, text="Excluir Comando", command=delete_command, font=("Arial", 10)).pack(side="left", padx=5)
    Button(button_frame, text="Reiniciar Bot", command=restart_bot, font=("Arial", 10)).pack(side="left", padx=5)

    qr_code_frame = Frame(frame_right, bg="#FFFFFF", relief="solid", borderwidth=2)
    qr_code_frame.pack(pady=10)

    Label(qr_code_frame, text="Escaneie o QR Code para conectar", font=("Arial", 10), bg="#FFFFFF", fg="#333").pack()
    qr_code_label = Label(qr_code_frame, text="QR Code será exibido aqui", font=("Arial", 12), bg="#FFFFFF", fg="#666")
    qr_code_label.pack(padx=10, pady=10)

    ttk.Label(frame_right, text="Comandos Configurados:", font=("Arial", 11)).pack(anchor="w", padx=10, pady=5)
    command_list_frame = Frame(frame_right)
    command_list_frame.pack(fill="both", expand=True, pady=5)

    command_list = Listbox(command_list_frame, font=("Arial", 10), width=40, height=15)
    command_list.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(command_list_frame, orient="vertical", command=command_list.yview)
    scrollbar.pack(side="right", fill="y")
    command_list.config(yscrollcommand=scrollbar.set)

    footer = Label(root, text="Propriedade da Astec Celulares - Todos os direitos reservados © 2025", 
                   font=("Arial", 10), bg="#333333", fg="#FFFFFF", pady=5)
    footer.pack(side="bottom", fill="x")

    update_command_list()
    threading.Thread(target=display_qr_code, daemon=True).start()
    threading.Thread(target=update_status, daemon=True).start()
    root.mainloop()

# Função principal
def main():
    threading.Thread(target=start_bot, daemon=True).start()
    start_interface()

if __name__ == "__main__":
    main()
