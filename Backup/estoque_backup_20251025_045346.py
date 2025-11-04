"""
Módulo de Controle de Estoque
Sistema completo para cadastro e gerenciamento de produtos
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import re
from datetime import datetime
from modules.db import conectar
from PIL import Image, ImageTk
import os

class TelaEstoque(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Paleta de cores corporativa (baseada no padrão do dashboard)
        self.colors = {
            'primary': '#1f538d',           # Azul corporativo principal
            'primary_hover': '#14375e',     # Azul hover
            'secondary': '#2b2b2b',         # Cinza escuro secundário
            'background': '#1a1a1a',        # Fundo escuro (sidebar_bg_dashboard - WCAG AA ✅)
            'card_bg': '#2b2b2b',           # Fundo dos cards (escuro)
            'text_primary': '#ffffff',      # Texto principal claro (para fundo escuro)
            'text_secondary': '#cccccc',    # Texto secundário claro
            'text_light': '#ffffff',        # Texto claro
            'text_dark': '#2b2b2b',         # Texto escuro (para fundos claros)
            'success': '#1e7e34',           # Verde para sucesso (ajustado para WCAG AA)
            'success_hover': '#155724',     # Verde hover (mais escuro)
            'warning': '#ffc107',           # Amarelo para avisos
            'warning_hover': '#e0a800',     # Amarelo hover
            'danger': '#dc3545',            # Vermelho para perigo
            'danger_hover': '#c82333',      # Vermelho hover
            'neutral': '#6c757d',           # Cinza neutro
            'neutral_hover': '#5a6268',     # Cinza neutro hover
            'border': '#404040',            # Bordas escuras
            'input_bg': '#343a40',          # Fundo dos inputs (escuro)
            'accent': '#0078d4'             # Azul de destaque
        }
        
        # Configurações da tela
        self.configure(fg_color=self.colors['background'])
        
        # Variáveis do formulário
        self.setup_variables()
        
        # Criar interface
        self.create_form_sections()
        
        # Carregar dados iniciais
        self.load_categories()
        self.load_suppliers()
        
    def setup_variables(self):
        """Inicializa as variáveis do formulário"""
        # Informações básicas
        self.nome_var = ctk.StringVar()
        self.descricao_var = ctk.StringVar()
        self.categoria_var = ctk.StringVar()
        self.codigo_barras_var = ctk.StringVar()
        
        # Estoque
        self.quantidade_var = ctk.StringVar(value="0")
        self.estoque_minimo_var = ctk.StringVar(value="0")
        self.localizacao_var = ctk.StringVar()
        
        # Preços
        self.preco_custo_var = ctk.StringVar(value="0,00")
        self.preco_venda_var = ctk.StringVar(value="0,00")
        self.margem_lucro_var = ctk.StringVar(value="0,00%")
        
        # Fornecedor
        self.fornecedor_var = ctk.StringVar()
        self.info_fornecedor_var = ctk.StringVar()
        
        # Imagem
        self.imagem_path = None
        self.current_photo = None  # Referência para a imagem atual
        
    def create_header(self):
        """Cria o cabeçalho da tela"""
        header_frame = ctk.CTkFrame(self, height=80, fg_color=self.colors['primary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="📦 Cadastro de Produtos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['text_light']
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Botão de ajuda
        help_btn = ctk.CTkButton(
            header_frame,
            text="❓ Ajuda",
            width=100,
            height=40,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary_hover'],
            text_color=self.colors['text_light'],
            command=self.show_help
        )
        help_btn.pack(side="right", padx=20, pady=20)
        
    def create_form_sections(self):
        """Cria todas as seções do formulário"""
        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Container para as seções
        sections_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        sections_container.pack(fill="both", expand=True)
        
        # Grid de 2 colunas
        sections_container.grid_columnconfigure(0, weight=1)
        sections_container.grid_columnconfigure(1, weight=1)
        
        # Seção 1: Informações Básicas
        self.create_basic_info_section(sections_container, row=0, column=0)
        
        # Seção 2: Estoque
        self.create_stock_section(sections_container, row=0, column=1)
        
        # Seção 3: Preços
        self.create_price_section(sections_container, row=1, column=0)
        
        # Seção 4: Fornecedor
        self.create_supplier_section(sections_container, row=1, column=1)
        
        # Seção 5: Imagem
        self.create_image_section(sections_container, row=2, column=0)
        
        # Seção 6: Controles
        self.create_controls_section(sections_container, row=2, column=1)
        
    def create_basic_info_section(self, parent, row, column):
        """Cria a seção de informações básicas"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Título da seção
        section_title = ctk.CTkLabel(
            section_frame,
            text="📋 Informações Básicas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        section_title.pack(pady=(20, 15))
        
        # Nome do produto (obrigatório)
        self.create_field(
            section_frame,
            "Nome do Produto *",
            self.nome_var,
            placeholder="Digite o nome do produto"
        )
        
        # Descrição
        desc_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        desc_frame.pack(fill="x", padx=20, pady=5)
        
        desc_label = ctk.CTkLabel(desc_frame, text="Descrição:", font=("Arial", 14, "bold"))
        desc_label.pack(anchor="w", pady=(0, 5))
        
        self.descricao_entry = ctk.CTkTextbox(
            desc_frame,
            height=80
        )
        self.descricao_entry.pack(fill="x", pady=(0, 10))
        self.descricao_entry.insert("1.0", "Descrição detalhada do produto")
        
        # Categoria
        self.categoria_combo = self.create_combobox(
            section_frame,
            "Categoria *",
            self.categoria_var,
            []
        )
        
        # Código de barras
        codigo_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        codigo_frame.pack(fill="x", padx=20, pady=5)
        
        codigo_label = ctk.CTkLabel(codigo_frame, text="Código de Barras/EAN", font=ctk.CTkFont(size=14, weight="bold"))
        codigo_label.pack(anchor="w")
        
        codigo_input_frame = ctk.CTkFrame(codigo_frame, fg_color="transparent")
        codigo_input_frame.pack(fill="x", pady=(5, 0))
        
        self.codigo_entry = ctk.CTkEntry(
            codigo_input_frame,
            textvariable=self.codigo_barras_var,
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border']
        )
        self.codigo_entry.pack(side="left", fill="x", expand=True)
        self.codigo_entry.insert(0, "Digite ou escaneie o código")
        
        validate_btn = ctk.CTkButton(
            codigo_input_frame,
            text="✓",
            width=40,
            fg_color=self.colors['success'],
            hover_color=self.colors['success_hover'],
            text_color=self.colors['text_light'],
            command=self.validate_barcode
        )
        validate_btn.pack(side="right", padx=(10, 0))
        
    def create_stock_section(self, parent, row, column):
        """Cria a seção de estoque"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Quantidade inicial
        self.create_numeric_field(
            section_frame,
            "Quantidade Inicial",
            self.quantidade_var
        )
        
        # Estoque mínimo
        self.create_numeric_field(
            section_frame,
            "Estoque Mínimo",
            self.estoque_minimo_var
        )
        
        # Localização
        self.create_field(
            section_frame,
            "Localização no Armazém",
            self.localizacao_var,
            placeholder="Ex: Prateleira A-1, Setor B"
        )
        
    def create_price_section(self, parent, row, column):
        """Cria a seção de preços"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Título da seção
        title = ctk.CTkLabel(
            section_frame,
            text="💰 Preços e Margem",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=(20, 15))
        
        # Preço de custo
        self.preco_custo_entry = self.create_money_field(
            section_frame,
            "Preço de Custo *",
            self.preco_custo_var
        )
        
        # Preço de venda
        self.preco_venda_entry = self.create_money_field(
            section_frame,
            "Preço de Venda *",
            self.preco_venda_var
        )
        
        # Margem de lucro (calculada)
        margem_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        margem_frame.pack(fill="x", padx=20, pady=5)
        
        margem_label = ctk.CTkLabel(
            margem_frame, 
            text="Margem de Lucro", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        margem_label.pack(anchor="w")
        
        self.margem_entry = ctk.CTkEntry(
            margem_frame,
            textvariable=self.margem_lucro_var,
            state="readonly",
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['success']
        )
        self.margem_entry.pack(fill="x", pady=(5, 0))
        
        # Bind para calcular margem automaticamente
        self.preco_custo_var.trace("w", self.calculate_margin)
        self.preco_venda_var.trace("w", self.calculate_margin)
        
    def create_supplier_section(self, parent, row, column):
        """Cria a seção de fornecedor"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Título da seção
        title = ctk.CTkLabel(
            section_frame,
            text="🏢 Fornecedor",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=(20, 15))
        
        # Seleção de fornecedor
        self.fornecedor_combo = self.create_combobox(
            section_frame,
            "Fornecedor Principal",
            self.fornecedor_var,
            []
        )
        
        # Informações adicionais
        info_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=5)
        
        info_label = ctk.CTkLabel(
            info_frame, 
            text="Informações Adicionais", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        info_label.pack(anchor="w")
        
        self.info_fornecedor_entry = ctk.CTkTextbox(
            info_frame,
            height=80,
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border']
        )
        self.info_fornecedor_entry.pack(fill="x", pady=(5, 0))
        self.info_fornecedor_entry.insert("1.0", "Observações sobre o fornecedor")
        
    def create_image_section(self, parent, row, column):
        """Cria a seção de imagem"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Título da seção
        title = ctk.CTkLabel(
            section_frame,
            text="🖼️ Imagem do Produto",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=(20, 15))
        
        # Preview da imagem
        self.image_preview = ctk.CTkLabel(
            section_frame,
            text="📷\nNenhuma imagem\nselecionada",
            width=200,
            height=150,
            fg_color=self.colors['background'],
            text_color=self.colors['text_secondary'],
            corner_radius=10
        )
        self.image_preview.pack(pady=10)
        
        # Botões de imagem
        image_buttons_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        image_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        upload_btn = ctk.CTkButton(
            image_buttons_frame,
            text="📁 Selecionar Imagem",
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            text_color=self.colors['text_light'],
            command=self.select_image
        )
        upload_btn.pack(side="left", padx=(0, 10))
        
        remove_btn = ctk.CTkButton(
            image_buttons_frame,
            text="🗑️ Remover",
            fg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            text_color=self.colors['text_light'],
            command=self.remove_image
        )
        remove_btn.pack(side="left")
        
    def create_controls_section(self, parent, row, column):
        """Cria a seção de controles"""
        section_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        section_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Título da seção
        title = ctk.CTkLabel(
            section_frame,
            text="⚙️ Ações",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=(20, 15))
        
        # Botões principais
        buttons_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão Salvar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar Produto",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=self.colors['success_hover'],
            text_color=self.colors['text_light'],
            command=self.save_product
        )
        save_btn.pack(fill="x", pady=(0, 10))
        
        # Botão Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            height=40,
            fg_color=self.colors['neutral'],
            hover_color=self.colors['neutral_hover'],
            text_color=self.colors['text_light'],
            command=self.clear_form
        )
        cancel_btn.pack(fill="x", pady=(0, 10))
        
        # Botão Limpar
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🧹 Limpar Formulário",
            height=40,
            fg_color=self.colors['warning'],
            hover_color=self.colors['warning_hover'],
            text_color=self.colors['text_primary'],
            command=self.clear_form
        )
        clear_btn.pack(fill="x")
        
    def create_field(self, parent, label_text, variable, placeholder=""):
        """Cria um campo de entrada padrão"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=5)
        
        label = ctk.CTkLabel(
            field_frame, 
            text=label_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        label.pack(anchor="w")
        
        entry = ctk.CTkEntry(
            field_frame,
            textvariable=variable,
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border']
        )
        entry.pack(fill="x", pady=(5, 0))
        
        if placeholder:
            entry.insert(0, placeholder)
        
        return entry
        
    def create_numeric_field(self, parent, label_text, variable):
        """Cria um campo numérico"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=5)
        
        label = ctk.CTkLabel(
            field_frame, 
            text=label_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        label.pack(anchor="w")
        
        entry = ctk.CTkEntry(
            field_frame,
            textvariable=variable,
            justify="right",
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border']
        )
        entry.pack(fill="x", pady=(5, 0))
        
        # Validação numérica
        entry.bind("<KeyRelease>", lambda e: self.validate_numeric(variable))
        
        return entry
        
    def create_money_field(self, parent, label_text, variable):
        """Cria um campo monetário com máscara"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=5)
        
        label = ctk.CTkLabel(
            field_frame, 
            text=label_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        label.pack(anchor="w")
        
        money_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        money_frame.pack(fill="x", pady=(5, 0))
        
        currency_label = ctk.CTkLabel(
            money_frame, 
            text="R$", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        currency_label.pack(side="left", padx=(0, 5))
        
        entry = ctk.CTkEntry(
            money_frame,
            textvariable=variable,
            justify="right",
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border']
        )
        entry.pack(side="left", fill="x", expand=True)
        
        # Aplicar máscara monetária
        entry.bind("<KeyRelease>", lambda e: self.apply_money_mask(variable))
        
        return entry
        
    def create_combobox(self, parent, label_text, variable, values):
        """Cria um combobox"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=5)
        
        label = ctk.CTkLabel(
            field_frame, 
            text=label_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        label.pack(anchor="w")
        
        combo = ctk.CTkComboBox(
            field_frame,
            variable=variable,
            values=values,
            state="readonly",
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border'],
            button_color=self.colors['primary'],
            button_hover_color=self.colors['primary_hover']
        )
        combo.pack(fill="x", pady=(5, 0))
        
        return combo
        
    def load_categories(self):
        """Carrega as categorias disponíveis"""
        categories = [
            "Alimentação",
            "Bebidas",
            "Limpeza",
            "Higiene",
            "Eletrônicos",
            "Roupas",
            "Calçados",
            "Casa e Jardim",
            "Esportes",
            "Livros",
            "Brinquedos",
            "Outros"
        ]
        self.categoria_combo.configure(values=categories)
        
    def load_suppliers(self):
        """Carrega os fornecedores do banco de dados"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM fornecedores ORDER BY nome")
            suppliers = cursor.fetchall()
            conn.close()
            
            supplier_list = [f"{supplier[1]} (ID: {supplier[0]})" for supplier in suppliers]
            self.fornecedor_combo.configure(values=supplier_list)
            
        except Exception as e:
            print(f"Erro ao carregar fornecedores: {e}")
            
    def validate_numeric(self, variable):
        """Valida entrada numérica"""
        value = variable.get()
        # Remove caracteres não numéricos
        numeric_value = re.sub(r'[^\d]', '', value)
        if value != numeric_value:
            variable.set(numeric_value)
            
    def apply_money_mask(self, variable):
        """Aplica máscara monetária"""
        value = variable.get().replace(',', '').replace('.', '')
        # Remove caracteres não numéricos
        numeric_value = re.sub(r'[^\d]', '', value)
        
        if numeric_value:
            # Converte para formato monetário
            if len(numeric_value) == 1:
                formatted = f"0,0{numeric_value}"
            elif len(numeric_value) == 2:
                formatted = f"0,{numeric_value}"
            else:
                formatted = f"{numeric_value[:-2]},{numeric_value[-2:]}"
            variable.set(formatted)
        else:
            variable.set("0,00")
            
    def calculate_margin(self, *args):
        """Calcula a margem de lucro automaticamente"""
        try:
            custo_str = self.preco_custo_var.get().replace(',', '.')
            venda_str = self.preco_venda_var.get().replace(',', '.')
            
            custo = float(custo_str) if custo_str else 0
            venda = float(venda_str) if venda_str else 0
            
            if custo > 0:
                margem = ((venda - custo) / custo) * 100
                self.margem_lucro_var.set(f"{margem:.2f}%")
            else:
                self.margem_lucro_var.set("0,00%")
                
        except ValueError:
            self.margem_lucro_var.set("0,00%")
            
    def validate_barcode(self):
        """Valida o código de barras"""
        codigo = self.codigo_barras_var.get().strip()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um código de barras para validar.")
            return
            
        # Validação básica de EAN-13
        if len(codigo) == 13 and codigo.isdigit():
            messagebox.showinfo("Sucesso", "Código de barras válido!")
        elif len(codigo) == 8 and codigo.isdigit():
            messagebox.showinfo("Sucesso", "Código EAN-8 válido!")
        else:
            messagebox.showwarning("Aviso", "Código de barras inválido. Use EAN-8 (8 dígitos) ou EAN-13 (13 dígitos).")
            
    def select_image(self):
        """Seleciona uma imagem para o produto"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem do Produto",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.imagem_path = file_path
            self.update_image_preview()
            
    def update_image_preview(self):
        """Atualiza o preview da imagem"""
        if self.imagem_path and os.path.exists(self.imagem_path):
            try:
                # Carregar e redimensionar imagem
                image = Image.open(self.imagem_path)
                image = image.resize((180, 130), Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Armazenar referência da imagem na instância da classe
                self.current_photo = photo
                
                # Atualizar preview
                self.image_preview.configure(image=photo, text="")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")
                
    def remove_image(self):
        """Remove a imagem selecionada"""
        self.imagem_path = None
        self.current_photo = None  # Limpar referência da imagem
        self.image_preview.configure(
            image=None,
            text="📷\nNenhuma imagem\nselecionada"
        )
        
    def validate_form(self):
        """Valida o formulário antes de salvar"""
        errors = []
        
        # Campos obrigatórios
        if not self.nome_var.get().strip():
            errors.append("Nome do produto é obrigatório")
            
        if not self.categoria_var.get():
            errors.append("Categoria é obrigatória")
            
        # Validar preços
        try:
            custo = float(self.preco_custo_var.get().replace(',', '.'))
            if custo <= 0:
                errors.append("Preço de custo deve ser maior que zero")
        except ValueError:
            errors.append("Preço de custo inválido")
            
        try:
            venda = float(self.preco_venda_var.get().replace(',', '.'))
            if venda <= 0:
                errors.append("Preço de venda deve ser maior que zero")
        except ValueError:
            errors.append("Preço de venda inválido")
            
        # Validar código de barras se preenchido
        codigo = self.codigo_barras_var.get().strip()
        if codigo and not (len(codigo) in [8, 13] and codigo.isdigit()):
            errors.append("Código de barras deve ter 8 ou 13 dígitos")
            
        return errors
        
    def save_product(self):
        """Salva o produto no banco de dados"""
        # Validar formulário
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Erro de Validação", "\n".join(errors))
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Extrair ID do fornecedor
            fornecedor_id = None
            if self.fornecedor_var.get():
                fornecedor_text = self.fornecedor_var.get()
                if "ID: " in fornecedor_text:
                    fornecedor_id = int(fornecedor_text.split("ID: ")[1].split(")")[0])
            
            # Preparar dados
            dados = (
                self.nome_var.get().strip(),
                self.descricao_entry.get("1.0", "end-1c"),
                self.categoria_var.get(),
                self.codigo_barras_var.get().strip() or None,
                int(self.quantidade_var.get() or 0),
                int(self.estoque_minimo_var.get() or 0),
                self.localizacao_var.get().strip(),
                float(self.preco_custo_var.get().replace(',', '.')),
                float(self.preco_venda_var.get().replace(',', '.')),
                float(self.margem_lucro_var.get().replace('%', '').replace(',', '.')),
                fornecedor_id,
                self.imagem_path
            )
            
            # Inserir no banco
            cursor.execute("""
                INSERT INTO produtos (
                    nome, descricao, categoria, codigo_barras, quantidade,
                    estoque_minimo, localizacao, preco_custo, preco_venda,
                    margem_lucro, fornecedor_id, imagem_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.clear_form()
            
        except sqlite3.IntegrityError as e:
            if "codigo_barras" in str(e):
                messagebox.showerror("Erro", "Código de barras já existe no sistema!")
            else:
                messagebox.showerror("Erro", f"Erro de integridade: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {e}")
            
    def clear_form(self):
        """Limpa todos os campos do formulário"""
        # Limpar variáveis
        self.nome_var.set("")
        self.categoria_var.set("")
        self.codigo_barras_var.set("")
        self.quantidade_var.set("0")
        self.estoque_minimo_var.set("0")
        self.localizacao_var.set("")
        self.preco_custo_var.set("0,00")
        self.preco_venda_var.set("0,00")
        self.margem_lucro_var.set("0,00%")
        self.fornecedor_var.set("")
        
        # Limpar campos de texto
        self.descricao_entry.delete("1.0", "end")
        self.info_fornecedor_entry.delete("1.0", "end")
        
        # Remover imagem
        self.remove_image()
        
    def show_help(self):
        """Mostra ajuda sobre o cadastro de produtos"""
        help_text = """
        📋 AJUDA - CADASTRO DE PRODUTOS
        
        🔹 CAMPOS OBRIGATÓRIOS:
        • Nome do Produto
        • Categoria
        • Preço de Custo
        • Preço de Venda
        
        🔹 CÓDIGO DE BARRAS:
        • Use EAN-8 (8 dígitos) ou EAN-13 (13 dígitos)
        • Clique em "✓" para validar
        
        🔹 PREÇOS:
        • A margem de lucro é calculada automaticamente
        • Use vírgula para decimais (ex: 10,50)
        
        🔹 IMAGEM:
        • Formatos aceitos: PNG, JPG, JPEG, GIF, BMP
        • Tamanho recomendado: até 2MB
        
        🔹 DICAS:
        • Preencha a localização para facilitar a busca
        • Configure o estoque mínimo para alertas
        • Use descrições detalhadas para melhor identificação
        """
        
        messagebox.showinfo("Ajuda", help_text)


# Função para testar o módulo
if __name__ == "__main__":
    # Configurar o tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar as tabelas se não existirem
    from modules.db import criar_tabelas
    criar_tabelas()
    
    # Executar a aplicação
    app = ctk.CTk()
    app.title("Teste - Cadastro de Produtos")
    app.geometry("1400x900")
    
    estoque = TelaEstoque(app)
    estoque.pack(fill="both", expand=True)
    
    app.mainloop()