import tkinter as tk
from tkinter import messagebox

class AssistenciaTecnicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão - ASTEC Celulares")
        self.root.geometry("800x600")

        # Configurar layout
        self.create_menu()
        self.create_main_screen()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # Menu de Clientes
        clientes_menu = tk.Menu(menu_bar, tearoff=0)
        clientes_menu.add_command(label="Cadastrar Cliente", command=self.cadastrar_cliente)
        clientes_menu.add_command(label="Listar Clientes", command=self.listar_clientes)
        menu_bar.add_cascade(label="Clientes", menu=clientes_menu)

        # Menu de Ordens de Serviço
        os_menu = tk.Menu(menu_bar, tearoff=0)
        os_menu.add_command(label="Criar Ordem de Serviço", command=self.criar_ordem_servico)
        os_menu.add_command(label="Listar Ordens de Serviço", command=self.listar_ordens_servico)
        menu_bar.add_cascade(label="Ordens de Serviço", menu=os_menu)

        # Menu de Configurações
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Sobre", command=self.sobre)
        menu_bar.add_cascade(label="Configurações", menu=config_menu)

        self.root.config(menu=menu_bar)

    def create_main_screen(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        label_bem_vindo = tk.Label(self.main_frame, text="Bem-vindo ao Sistema de Gestão da ASTEC Celulares!", font=("Helvetica", 16))
        label_bem_vindo.pack(pady=20)

    def cadastrar_cliente(self):
        messagebox.showinfo("Cadastrar Cliente", "Função de cadastro de cliente em desenvolvimento!")

    def listar_clientes(self):
        messagebox.showinfo("Listar Clientes", "Função de listar clientes em desenvolvimento!")

    def criar_ordem_servico(self):
        messagebox.showinfo("Criar Ordem de Serviço", "Função de criar ordem de serviço em desenvolvimento!")

    def listar_ordens_servico(self):
        messagebox.showinfo("Listar Ordens de Serviço", "Função de listar ordens de serviço em desenvolvimento!")

    def sobre(self):
        messagebox.showinfo("Sobre", "Sistema de Gestão - ASTEC Celulares\nVersão 1.0\nDesenvolvido por ASTEC Celulares.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistenciaTecnicaApp(root)
    root.mainloop()
