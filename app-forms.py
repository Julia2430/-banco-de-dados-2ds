import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class SistemaCadastroClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("430x280")
        self.root.resizable(False, False)

        # Inicializa o banco de dados
        self.conectar_banco()

        # Cria os elementos da interface
        self.criar_widgets()

    def conectar_banco(self):
        """Cria a conexão com o SQLite e a tabela caso não exista."""
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def criar_widgets(self):
        """Monta o formulário na janela principal."""
        titulo = tk.Label(self.root, text="Cadastro de Clientes", font=("Arial", 16, "bold"))
        titulo.pack(pady=15)

        frame_campos = tk.Frame(self.root)
        frame_campos.pack(pady=5, padx=20, fill="x")

        # Campo Nome
        tk.Label(frame_campos, text="Nome:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_campos, width=38, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10)

        # Campo E-mail
        tk.Label(frame_campos, text="E-mail:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame_campos, width=38, font=("Arial", 10))
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)

        # Campo Telefone
        tk.Label(frame_campos, text="Telefone:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_telefone = tk.Entry(frame_campos, width=38, font=("Arial", 10))
        self.entry_telefone.grid(row=2, column=1, pady=5, padx=10)

        # Frame para os botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=20)

        btn_salvar = tk.Button(
            frame_botoes, text="Salvar", width=11, bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"), command=self.salvar_cliente
        )
        btn_salvar.grid(row=0, column=0, padx=6)

        btn_limpar = tk.Button(
            frame_botoes, text="Limpar", width=11, bg="#f44336", fg="white",
            font=("Arial", 10, "bold"), command=self.limpar_formulario
        )
        btn_limpar.grid(row=0, column=1, padx=6)

        # NOVO BOTÃO: Visualizar Clientes
        btn_visualizar = tk.Button(
            frame_botoes, text="Visualizar Clientes", width=16, bg="#2196F3", fg="white",
            font=("Arial", 10, "bold"), command=self.visualizar_clientes
        )
        btn_visualizar.grid(row=0, column=2, padx=6)

    def salvar_cliente(self):
        """Valida os dados e insere no banco SQLite."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome or not email or not telefone:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos antes de salvar.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("E-mail Inválido", "Por favor, insira um endereço de e-mail válido.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone)
            )
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
            self.limpar_formulario()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao salvar: {erro}")

    def limpar_formulario(self):
        """Apaga o conteúdo de todos os campos e devolve o foco ao campo Nome."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_nome.focus()

    # NOVA FUNCIONALIDADE: Visualizar Clientes
    def visualizar_clientes(self):
        """Abre uma nova janela exibindo todos os clientes cadastrados."""
        try:
            self.cursor.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY id ASC")
            registros = self.cursor.fetchall()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível carregar os dados: {erro}")
            return

        # Cria a janela secundária
        janela_lista = tk.Toplevel(self.root)
        janela_lista.title("Clientes Cadastrados")
        janela_lista.geometry("620x350")
        janela_lista.grab_set()  # Mantém o foco na janela aberta

        tk.Label(janela_lista, text="Lista de Clientes Cadastrados", font=("Arial", 14, "bold")).pack(pady=10)

        # Frame para comportar a tabela e a barra de rolagem
        frame_tabela = tk.Frame(janela_lista)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Configuração da tabela (Treeview)
        colunas = ("id", "nome", "email", "telefone")
        tabela = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tabela.yview)

        # Cabeçalhos das colunas
        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome")
        tabela.heading("email", text="E-mail")
        tabela.heading("telefone", text="Telefone")

        # Largura e alinhamento das colunas
        tabela.column("id", width=50, anchor="center")
        tabela.column("nome", width=200, anchor="w")
        tabela.column("email", width=200, anchor="w")
        tabela.column("telefone", width=120, anchor="center")

        # Preenche a tabela com os registros do banco
        for cliente in registros:
            tabela.insert("", tk.END, values=cliente)

        tabela.pack(fill="both", expand=True)

        # Rodapé informativo e botão de fechar
        total = len(registros)
        tk.Label(
            janela_lista, text=f"Total de clientes cadastrados: {total}", font=("Arial", 9, "italic")
        ).pack(pady=5)

        btn_fechar = tk.Button(
            janela_lista, text="Fechar", width=12, command=janela_lista.destroy
        )
        btn_fechar.pack(pady=8)

    def fechar_janela(self):
        """Fecha a conexão com o banco antes de encerrar o programa."""
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCadastroClientes(janela)
    janela.protocol("WM_DELETE_WINDOW", app.fechar_janela)
    janela.mainloop()
