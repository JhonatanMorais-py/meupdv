# Tela principal do dashboard com layout sidebar
import customtkinter as ctk
from tkinter import messagebox
from modules import vendas, clientes, produtos, estoque, relatorios


class TelaDashboard(ctk.CTk):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.usuario_logado = usuario_logado
        self.current_module = None
        self.title("PDV - Dashboard Principal")
        self.geometry("1200x700")
        self.minsize(800, 600)
        ctk.set_appearance_mode("dark")
        
        # Cores do tema
        self.colors = {
            'primary': '#1f538d',
            'primary_hover': '#14375e',
            'secondary': '#2b2b2b',
            'sidebar_bg': '#1a1a1a',
            'content_bg': '#2b2b2b',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'accent': '#0078d4'
        }
        
        # Configurar layout principal
        self.setup_layout()
        self.create_sidebar()
        self.create_content_area()
        
        # Selecionar primeiro item por padrão
        self.select_module("dashboard")
    
    def setup_layout(self):
        """Configura o layout principal com sidebar e área de conteúdo"""
        # Configurar grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame da sidebar (coluna 0)
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=250, 
            corner_radius=0,
            fg_color=self.colors['sidebar_bg']
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # Frame do conteúdo principal (coluna 1)
        self.content_frame = ctk.CTkFrame(
            self, 
            corner_radius=0,
            fg_color=self.colors['content_bg']
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
    
    def create_sidebar(self):
        """Cria a sidebar com navegação dos módulos"""
        # Header da sidebar
        header_frame = ctk.CTkFrame(
            self.sidebar_frame, 
            height=80, 
            corner_radius=0,
            fg_color=self.colors['primary']
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 PDV System",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(pady=20)
        
        # Informações do usuário
        user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            height=60,
            corner_radius=8,
            fg_color=self.colors['secondary']
        )
        user_frame.pack(fill="x", padx=15, pady=15)
        user_frame.pack_propagate(False)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.usuario_logado or 'Usuário'}",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        user_label.pack(pady=15)
        
        # Separador
        separator = ctk.CTkFrame(
            self.sidebar_frame,
            height=2,
            corner_radius=0,
            fg_color=self.colors['secondary']
        )
        separator.pack(fill="x", padx=15, pady=(0, 15))
        
        # Lista de módulos
        self.create_navigation_menu()
        
        # Botão de logout no final
        logout_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🚪 Sair",
            command=self.fazer_logout,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            text_color=self.colors['text_secondary'],
            hover_color=("#ff4444", "#cc3333"),
            font=ctk.CTkFont(size=14)
        )
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=15)
    
    def create_navigation_menu(self):
        """Cria o menu de navegação com os módulos"""
        # Container para os itens do menu
        self.menu_frame = ctk.CTkFrame(
            self.sidebar_frame,
            corner_radius=0,
            fg_color="transparent"
        )
        self.menu_frame.pack(fill="both", expand=True, padx=15)
        
        # Lista de módulos disponíveis
        self.modules = [
            {"name": "dashboard", "label": "🏠 Dashboard", "icon": "🏠"},
            {"name": "vendas", "label": "💰 Vendas", "icon": "💰"},
            {"name": "produtos", "label": "📦 Produtos", "icon": "📦"},
            {"name": "clientes", "label": "👥 Clientes", "icon": "👥"},
            {"name": "estoque", "label": "📊 Estoque", "icon": "📊"},
            {"name": "relatorios", "label": "📈 Relatórios", "icon": "📈"}
        ]
        
        # Criar botões para cada módulo
        self.menu_buttons = {}
        for module in self.modules:
            btn = self.create_menu_button(module)
            self.menu_buttons[module["name"]] = btn
    
    def create_menu_button(self, module):
        """Cria um botão de menu para um módulo específico"""
        btn = ctk.CTkButton(
            self.menu_frame,
            text=module["label"],
            command=lambda m=module["name"]: self.select_module(m),
            height=45,
            corner_radius=8,
            fg_color="transparent",
            text_color=self.colors['text_secondary'],
            hover_color=(self.colors['primary_hover'], self.colors['primary_hover']),
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        btn.pack(fill="x", pady=2)
        return btn
    
    def select_module(self, module_name):
        """Seleciona um módulo e atualiza a interface"""
        # Resetar cores de todos os botões
        for name, btn in self.menu_buttons.items():
            if name == module_name:
                btn.configure(
                    fg_color=self.colors['primary'],
                    text_color=self.colors['text_primary']
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors['text_secondary']
                )
        
        self.current_module = module_name
        self.update_content_area(module_name)
    
    def create_content_area(self):
        """Cria a área de conteúdo principal"""
        # Header do conteúdo
        self.content_header = ctk.CTkFrame(
            self.content_frame,
            height=80,
            corner_radius=0,
            fg_color=self.colors['secondary']
        )
        self.content_header.pack(fill="x", padx=0, pady=0)
        self.content_header.pack_propagate(False)
        
        # Título da seção atual
        self.section_title = ctk.CTkLabel(
            self.content_header,
            text="Dashboard Principal",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.section_title.pack(side="left", padx=30, pady=25)
        
        # Área de conteúdo principal
        self.main_content = ctk.CTkFrame(
            self.content_frame,
            corner_radius=0,
            fg_color="transparent"
        )
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)
    
    def update_content_area(self, module_name):
        """Atualiza a área de conteúdo baseada no módulo selecionado"""
        # Limpar conteúdo anterior
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Atualizar título
        module_titles = {
            "dashboard": "Dashboard Principal",
            "vendas": "Gestão de Vendas",
            "produtos": "Gestão de Produtos",
            "clientes": "Gestão de Clientes",
            "estoque": "Controle de Estoque",
            "relatorios": "Relatórios e Análises"
        }
        
        self.section_title.configure(text=module_titles.get(module_name, "Dashboard"))
        
        # Criar conteúdo específico do módulo
        if module_name == "dashboard":
            self.create_dashboard_content()
        elif module_name == "vendas":
            self.create_vendas_content()
        else:
            self.create_placeholder_content(module_name)
    
    def create_dashboard_content(self):
        """Cria o conteúdo do dashboard principal"""
        # Cards de resumo
        cards_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Configurar grid para cards
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Card de vendas
        self.create_summary_card(
            cards_frame, "💰", "Vendas Hoje", "R$ 1.250,00", 0
        )
        
        # Card de produtos
        self.create_summary_card(
            cards_frame, "📦", "Produtos", "156", 1
        )
        
        # Card de clientes
        self.create_summary_card(
            cards_frame, "👥", "Clientes", "89", 2
        )
        
        # Card de estoque baixo
        self.create_summary_card(
            cards_frame, "⚠️", "Estoque Baixo", "12", 3
        )
        
        # Área de ações rápidas
        actions_frame = ctk.CTkFrame(self.main_content)
        actions_frame.pack(fill="both", expand=True)
        
        actions_title = ctk.CTkLabel(
            actions_frame,
            text="Ações Rápidas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        actions_title.pack(pady=20)
        
        # Botões de ação rápida
        quick_actions_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        quick_actions_frame.pack(expand=True)
        
        # Grid para botões
        quick_actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Botão Nova Venda
        nova_venda_btn = ctk.CTkButton(
            quick_actions_frame,
            text="💰 Nova Venda",
            command=lambda: self.select_module("vendas"),
            height=80,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent']
        )
        nova_venda_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Botão Cadastrar Produto
        produto_btn = ctk.CTkButton(
            quick_actions_frame,
            text="📦 Cadastrar Produto",
            command=lambda: self.select_module("produtos"),
            height=80,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['primary']
        )
        produto_btn.grid(row=0, column=1, padx=20, pady=20)
        
        # Botão Ver Relatórios
        relatorio_btn = ctk.CTkButton(
            quick_actions_frame,
            text="📈 Ver Relatórios",
            command=lambda: self.select_module("relatorios"),
            height=80,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['primary']
        )
        relatorio_btn.grid(row=0, column=2, padx=20, pady=20)
    
    def create_summary_card(self, parent, icon, title, value, column):
        """Cria um card de resumo"""
        card = ctk.CTkFrame(parent, height=100)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        card.pack_propagate(False)
        
        # Ícone
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(pady=(15, 5))
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        title_label.pack()
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        value_label.pack(pady=(0, 15))
    
    def create_vendas_content(self):
        """Cria o conteúdo da seção de vendas"""
        # Botão para abrir tela de vendas completa
        open_vendas_btn = ctk.CTkButton(
            self.main_content,
            text="🚀 Abrir Tela de Vendas Completa",
            command=self.abrir_vendas_completa,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent']
        )
        open_vendas_btn.pack(pady=50)
        
        # Informações sobre vendas
        info_frame = ctk.CTkFrame(self.main_content)
        info_frame.pack(fill="both", expand=True, pady=20)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Aqui você pode gerenciar todas as vendas do sistema.\nClique no botão acima para abrir a interface completa de vendas.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        info_label.pack(expand=True)
    
    def create_placeholder_content(self, module_name):
        """Cria conteúdo placeholder para módulos em desenvolvimento"""
        placeholder_frame = ctk.CTkFrame(self.main_content)
        placeholder_frame.pack(fill="both", expand=True)
        
        # Ícone do módulo
        module_icons = {
            "produtos": "📦",
            "clientes": "👥",
            "estoque": "📊",
            "relatorios": "📈"
        }
        
        icon_label = ctk.CTkLabel(
            placeholder_frame,
            text=module_icons.get(module_name, "🔧"),
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(50, 20))
        
        # Título
        title_label = ctk.CTkLabel(
            placeholder_frame,
            text=f"Módulo {module_name.title()}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(pady=10)
        
        # Descrição
        desc_label = ctk.CTkLabel(
            placeholder_frame,
            text="Este módulo está em desenvolvimento.\nEm breve estará disponível com todas as funcionalidades.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        desc_label.pack(pady=20)
    
    def abrir_vendas_completa(self):
        """Abre a tela completa de vendas"""
        try:
            self.destroy()
            app = vendas.TelaVendas()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir vendas: {str(e)}")
    
    def fazer_logout(self):
        """Realiza o logout e retorna para a tela de login"""
        resposta = messagebox.askyesno("Logout", "Deseja realmente sair do sistema?")
        if resposta:
            self.destroy()
            # Importar aqui para evitar importação circular
            from modules.login import TelaLogin
            app = TelaLogin()
            app.mainloop()