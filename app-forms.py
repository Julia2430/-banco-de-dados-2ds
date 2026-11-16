import tkinter as tk
from tkinter import messagebox
import sqlite3

class SistemaCadastroClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("400x280")
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
        # Título
        titulo = tk.Label(self.root, text="Cadastro de Clientes", font=("Arial", 16, "bold"))
        titulo.pack(pady=15)

        # Frame para organizar os campos em grade (Grid)
        frame_campos = tk.Frame(self.root)
        frame_campos.pack(pady=5, padx=20, fill="x")

        # Campo Nome
        tk.Label(frame_campos, text="Nome:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_campos, width=35, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10)

        # Campo E-mail
        tk.Label(frame_campos, text="E-mail:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame_campos, width=35, font=("Arial", 10))
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)

        # Campo Telefone
        tk.Label(frame_campos, text="Telefone:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_telefone = tk.Entry(frame_campos, width=35, font=("Arial", 10))
        self.entry_telefone.grid(row=2, column=1, pady=5, padx=10)

        # Frame para os botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=20)

        btn_salvar = tk.Button(
            frame_botoes, text="Salvar", width=12, bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"), command=self.salvar_cliente
        )
        btn_salvar.grid(row=0, column=0, padx=10)

        btn_limpar = tk.Button(
            frame_botoes, text="Limpar", width=12, bg="#f44336", fg="white",
            font=("Arial", 10, "bold"), command=self.limpar_formulario
        )
        btn_limpar.grid(row=0, column=1, padx=10)

    def salvar_cliente(self):
        """Valida os dados e insere no banco SQLite."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        # Validação de campos vazios
        if not nome or not email or not telefone:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos antes de salvar.")
            return

        # Validação simples de formato de e-mail
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

    def fechar_janela(self):
        """Fecha a conexão com o banco antes de encerrar o programa."""
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCadastroClientes(janela)
    janela.protocol("WM_DELETE_WINDOW", app.fechar_janela)
    janela.mainloop()
