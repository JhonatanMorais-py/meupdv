import customtkinter as ctk
from tkinter import messagebox
from modules import db
from ui.dashbord import TelaDashboard


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - PDV")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")

        self.label_titulo = ctk.CTkLabel(
            self, text="PDV - Login", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_usuario.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(
            self, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=10)

        self.btn_login = ctk.CTkButton(
            self, text="Entrar", command=self.fazer_login)
        self.btn_login.pack(pady=20)

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Validação básica dos campos
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            # Redirecionamento para o dashboard com o usuário logado
            self.destroy()
            app = TelaDashboard(usuario_logado=usuario)
            app.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
