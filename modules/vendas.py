# Funções de Venda
import customtkinter as ctk
from tkinter import ttk, messagebox
from modules import db


class TelaVendas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDV - Vendas")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")

        self.produtos = self.carregar_produtos()
        self.total = 0.0

        # --- Layout ---
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(pady=10, fill="x")

        self.produto_var = ctk.StringVar(value=list(self.produtos.keys())[
                                         0] if self.produtos else "")
        self.combo_produto = ctk.CTkComboBox(frame_top, values=list(
            self.produtos.keys()), variable=self.produto_var)
        self.combo_produto.pack(side="left", padx=10)

        self.btn_add = ctk.CTkButton(
            frame_top, text="Adicionar", command=self.adicionar_produto)
        self.btn_add.pack(side="left")

        self.tree = ttk.Treeview(self, columns=(
            "produto", "preco"), show="headings", height=15)
        self.tree.heading("produto", text="Produto")
        self.tree.heading("preco", text="Preço (R$)")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.lbl_total = ctk.CTkLabel(
            self, text="Total: R$ 0.00", font=("Arial", 16, "bold"))
        self.lbl_total.pack(pady=10)

        self.btn_finalizar = ctk.CTkButton(
            self, text="Finalizar Venda", command=self.finalizar_venda)
        self.btn_finalizar.pack(pady=5)

    def carregar_produtos(self):
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, preco FROM produtos")
        produtos = {nome: preco for nome, preco in cursor.fetchall()}
        conn.close()
        return produtos

    def adicionar_produto(self):
        produto = self.produto_var.get()
        preco = self.produtos.get(produto, 0.0)

        if produto:
            self.tree.insert("", "end", values=(produto, f"{preco:.2f}"))
            self.total += preco
            self.lbl_total.configure(text=f"Total: R$ {self.total:.2f}")

    def finalizar_venda(self):
        if self.total == 0:
            messagebox.showwarning("Aviso", "Nenhum produto adicionado.")
            return

        from datetime import datetime
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (data, total) VALUES (?, ?)",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.total))
        conn.commit()
        conn.close()

        messagebox.showinfo("Venda Finalizada",
                            f"Venda registrada!\nTotal: R$ {self.total:.2f}")
        self.tree.delete(*self.tree.get_children())
        self.total = 0.0
        self.lbl_total.configure(text="Total: R$ 0.00")