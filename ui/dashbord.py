# Tela principal do dashboard com layout sidebar
import customtkinter as ctk
from tkinter import messagebox
from modules import vendas, clientes, produtos, estoque, relatorios
from modules.db import conectar
from datetime import datetime


class TelaDashboard(ctk.CTk):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.usuario_logado = usuario_logado
        self.current_module = None
        self.title("PDV - Dashboard Principal")
        self.geometry("1400x800")  # Aumentado para melhor visualização
        self.minsize(1000, 700)    # Tamanho mínimo maior
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
            width=280,  # Aumentado para melhor espaçamento
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
            "estoque": "Gestão de Inventário",
            "relatorios": "Relatórios e Análises"
        }
        
        self.section_title.configure(text=module_titles.get(module_name, "Dashboard"))
        
        # Criar conteúdo específico do módulo
        if module_name == "dashboard":
            self.create_dashboard_content()
        elif module_name == "vendas":
            self.create_vendas_content()
        elif module_name == "estoque":
            self.create_estoque_content()
        else:
            self.create_placeholder_content(module_name)
    
    def get_dashboard_data(self):
        """Obtém dados dinâmicos do banco de dados para o dashboard"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Verificar se as tabelas existem
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabelas = [tabela[0] for tabela in cursor.fetchall()]
            
            # Vendas de hoje
            if 'vendas' in tabelas:
                try:
                    cursor.execute("""
                        SELECT COALESCE(SUM(total), 0) 
                        FROM vendas 
                        WHERE DATE(data_venda) = DATE('now')
                    """)
                    vendas_hoje = cursor.fetchone()[0]
                except:
                    # Tentar com campo 'data' se 'data_venda' não existir
                    try:
                        cursor.execute("""
                            SELECT COALESCE(SUM(total), 0) 
                            FROM vendas 
                            WHERE DATE(data) = DATE('now')
                        """)
                        vendas_hoje = cursor.fetchone()[0]
                    except:
                        vendas_hoje = 0
            else:
                vendas_hoje = 0
            
            vendas_hoje_str = f"R$ {vendas_hoje:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            # Total de produtos
            if 'produtos' in tabelas:
                try:
                    cursor.execute("SELECT COUNT(*) FROM produtos")
                    total_produtos = cursor.fetchone()[0]
                except:
                    total_produtos = 0
            else:
                total_produtos = 0
            
            # Total de clientes (baseado em vendas únicas ou tabela clientes)
            total_clientes = 0
            if 'clientes' in tabelas:
                try:
                    cursor.execute("SELECT COUNT(*) FROM clientes")
                    total_clientes = cursor.fetchone()[0]
                except:
                    pass
            elif 'vendas' in tabelas:
                try:
                    cursor.execute("SELECT COUNT(DISTINCT cliente) FROM vendas WHERE cliente IS NOT NULL AND cliente != ''")
                    total_clientes = cursor.fetchone()[0]
                except:
                    pass
            
            # Produtos com estoque baixo
            estoque_baixo = 0
            if 'produtos' in tabelas:
                try:
                    # Tentar com campo 'quantidade'
                    cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade < 10")
                    estoque_baixo = cursor.fetchone()[0]
                except:
                    try:
                        # Tentar com campo 'estoque'
                        cursor.execute("SELECT COUNT(*) FROM produtos WHERE estoque < 10")
                        estoque_baixo = cursor.fetchone()[0]
                    except:
                        pass
            
            conn.close()
            
            return {
                'vendas_hoje': vendas_hoje_str,
                'produtos': str(total_produtos),
                'clientes': str(total_clientes),
                'estoque_baixo': str(estoque_baixo)
            }
            
        except Exception as e:
            print(f"Erro ao obter dados do dashboard: {e}")
            return {
                'vendas_hoje': "R$ 0,00",
                'produtos': "0",
                'clientes': "0",
                'estoque_baixo': "0"
            }

    def create_summary_card(self, parent, icon, title, value, color):
        """Cria um card de resumo com layout melhorado e estilização visual aprimorada"""
        # Frame principal do card com altura fixa e efeito de sombra
        card = ctk.CTkFrame(
            parent, 
            height=140,  # Aumentado para melhor proporção
            corner_radius=15,
            fg_color=color,
            border_width=1,
            border_color=("#E0E0E0", "#404040")
        )
        card.pack_propagate(False)  # Mantém altura fixa
        
        # Efeito hover (simulado com mudança de cor)
        def on_enter(event):
            # Escurecer a cor no hover
            darker_color = self.darken_color(color, 0.1)
            card.configure(fg_color=darker_color)
        
        def on_leave(event):
            card.configure(fg_color=color)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Frame interno para melhor controle do layout
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Container superior para ícone e valor
        top_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Ícone à esquerda
        icon_label = ctk.CTkLabel(
            top_frame, 
            text=icon, 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        icon_label.pack(side="left", anchor="w")
        
        # Valor à direita
        value_label = ctk.CTkLabel(
            top_frame, 
            text=value, 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
            wraplength=120,
            justify="right"
        )
        value_label.pack(side="right", anchor="e")
        
        # Título na parte inferior
        title_label = ctk.CTkLabel(
            inner_frame, 
            text=title, 
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="#E0E0E0",  # Cor branca com transparência simulada
            wraplength=180,
            justify="left"
        )
        title_label.pack(anchor="w", pady=(5, 0))
        
        return card
    
    def darken_color(self, hex_color, factor):
        """Escurece uma cor hexadecimal por um fator"""
        try:
            # Remove o # se presente
            hex_color = hex_color.lstrip('#')
            
            # Converte para RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Escurece cada componente
            r = max(0, int(r * (1 - factor)))
            g = max(0, int(g * (1 - factor)))
            b = max(0, int(b * (1 - factor)))
            
            # Converte de volta para hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color  # Retorna a cor original se houver erro
    
    def create_dashboard_content(self):
        """Cria o conteúdo do dashboard principal"""
        # Obter dados reais do banco
        dados = self.get_dashboard_data()
        
        # Cards de resumo com layout melhorado
        cards_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 30), padx=20)
        
        # Configurar grid para cards com espaçamento adequado
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cards")
        
        # Cores para os cards
        card_colors = [
            "#2E8B57",  # Verde para vendas
            "#4682B4",  # Azul para produtos
            "#9370DB",  # Roxo para clientes
            "#DC143C"   # Vermelho para estoque baixo
        ]
        
        # Card de vendas
        card_vendas = self.create_summary_card(
            cards_frame, "💰", "Vendas Hoje", dados['vendas_hoje'], card_colors[0]
        )
        card_vendas.grid(row=0, column=0, padx=12, pady=15, sticky="ew")
        
        # Card de produtos
        card_produtos = self.create_summary_card(
            cards_frame, "📦", "Produtos", dados['produtos'], card_colors[1]
        )
        card_produtos.grid(row=0, column=1, padx=12, pady=15, sticky="ew")
        
        # Card de clientes
        card_clientes = self.create_summary_card(
            cards_frame, "👥", "Clientes", dados['clientes'], card_colors[2]
        )
        card_clientes.grid(row=0, column=2, padx=12, pady=15, sticky="ew")
        
        # Card de estoque baixo
        card_estoque = self.create_summary_card(
            cards_frame, "⚠️", "Estoque Baixo", dados['estoque_baixo'], card_colors[3]
        )
        card_estoque.grid(row=0, column=3, padx=12, pady=15, sticky="ew")
        
        # Área de ações rápidas
        actions_frame = ctk.CTkFrame(self.main_content)
        actions_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        actions_title = ctk.CTkLabel(
            actions_frame,
            text="Ações Rápidas",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        )
        actions_title.pack(pady=(30, 20))
        
        # Botões de ação rápida
        quick_actions_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        quick_actions_frame.pack(expand=True, pady=20)
        
        # Grid para botões
        quick_actions_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="actions")
        
        # Botão Nova Venda
        nova_venda_btn = ctk.CTkButton(
            quick_actions_frame,
            text="💰 Nova Venda",
            command=lambda: self.select_module("vendas"),
            height=90,
            width=220,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent']
        )
        nova_venda_btn.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        
        # Botão Cadastrar Produto
        produto_btn = ctk.CTkButton(
            quick_actions_frame,
            text="📦 Cadastrar Produto",
            command=lambda: self.select_module("produtos"),
            height=90,
            width=220,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['primary']
        )
        produto_btn.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
        
        # Botão Ver Relatórios
        relatorio_btn = ctk.CTkButton(
            quick_actions_frame,
            text="📈 Ver Relatórios",
            command=lambda: self.select_module("relatorios"),
            height=90,
            width=220,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['primary']
        )
        relatorio_btn.grid(row=0, column=2, padx=15, pady=20, sticky="ew")
    
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
    
    def create_estoque_content(self):
        """Cria o conteúdo integrado do módulo de estoque"""
        try:
            # Importar o módulo de estoque
            from modules.estoque import TelaEstoque
            
            # Criar frame container para o estoque
            estoque_container = ctk.CTkFrame(
                self.main_content,
                corner_radius=0,
                fg_color="transparent"
            )
            estoque_container.pack(fill="both", expand=True)
            
            # Criar instância da tela de estoque integrada
            self.tela_estoque = TelaEstoque(estoque_container)
            self.tela_estoque.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Forçar atualização da interface
            self.update_idletasks()
            
        except Exception as e:
            print(f"Erro ao carregar módulo de estoque: {e}")
            # Criar mensagem de erro amigável
            error_frame = ctk.CTkFrame(self.main_content)
            error_frame.pack(fill="both", expand=True)
            
            error_icon = ctk.CTkLabel(
                error_frame,
                text="⚠️",
                font=ctk.CTkFont(size=48)
            )
            error_icon.pack(pady=(50, 20))
            
            error_title = ctk.CTkLabel(
                error_frame,
                text="Erro ao Carregar Módulo",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=self.colors['text_primary']
            )
            error_title.pack(pady=10)
            
            error_desc = ctk.CTkLabel(
                error_frame,
                text=f"Não foi possível carregar o módulo de estoque.\nDetalhes: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_secondary']
            )
            error_desc.pack(pady=20)
            
            # Botão para tentar novamente
            retry_btn = ctk.CTkButton(
                error_frame,
                text="🔄 Tentar Novamente",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=48,
                width=200,
                fg_color=self.colors['primary'],
                hover_color=self.colors['primary_hover'],
                text_color=self.colors['text_primary'],
                corner_radius=8,
                command=lambda: self.select_module("estoque"),
                cursor="hand2"
            )
            retry_btn.pack(pady=20)
    
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
        
        # Tratamento especial para o módulo estoque
        if module_name == "estoque":
            # Descrição específica para estoque
            desc_label = ctk.CTkLabel(
                placeholder_frame,
                text="Acesse o módulo completo de controle de estoque\ncom funcionalidades de cadastro e gerenciamento de produtos.",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_secondary']
            )
            desc_label.pack(pady=20)
            
            # Botão para acessar estoque completo
            btn_acessar_estoque = ctk.CTkButton(
                placeholder_frame,
                text="🏪 Acessar Estoque Completo",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=48,  # Altura mínima para acessibilidade
                width=280,
                fg_color=self.colors['primary'],
                hover_color=self.colors['primary_hover'],
                text_color=self.colors['text_primary'],
                corner_radius=8,
                command=self.abrir_estoque_completo,
                cursor="hand2"  # Cursor de mão para indicar clicável
            )
            btn_acessar_estoque.pack(pady=20)
            
            # Adicionar efeito de feedback visual ao botão
            def on_button_press(event):
                btn_acessar_estoque.configure(fg_color="#0f3a5f")  # Cor mais escura quando pressionado
            
            def on_button_release(event):
                btn_acessar_estoque.configure(fg_color=self.colors['primary_hover'])
            
            btn_acessar_estoque.bind("<Button-1>", on_button_press)
            btn_acessar_estoque.bind("<ButtonRelease-1>", on_button_release)
            
        else:
            # Descrição padrão para outros módulos
            desc_label = ctk.CTkLabel(
                placeholder_frame,
                text="Este módulo está em desenvolvimento.\nEm breve estará disponível com todas as funcionalidades.",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_secondary']
            )
            desc_label.pack(pady=20)
    
    def abrir_estoque_completo(self):
        """Abre a tela completa de estoque em uma nova janela com transição suave"""
        try:
            # Desabilitar botão temporariamente para evitar múltiplos cliques
            for widget in self.main_content.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkButton) and "Acessar Estoque" in child.cget("text"):
                            child.configure(state="disabled")
                            # Reabilitar após 1 segundo
                            self.after(1000, lambda: child.configure(state="normal"))
                            break
            
            # Importar e criar a tela de estoque
            from modules.estoque import TelaEstoque
            
            # Criar nova janela para o estoque
            estoque_window = ctk.CTkToplevel(self)
            estoque_window.title("Sistema PDV - Gestão de Estoque")
            estoque_window.geometry("1200x800")
            estoque_window.resizable(True, True)
            
            # Configurar ícone se disponível
            try:
                estoque_window.iconbitmap("assets/icon.ico")
            except:
                pass
            
            # Centralizar janela na tela
            estoque_window.update_idletasks()
            x = (estoque_window.winfo_screenwidth() // 2) - (1200 // 2)
            y = (estoque_window.winfo_screenheight() // 2) - (800 // 2)
            estoque_window.geometry(f"1200x800+{x}+{y}")
            
            # Criar instância da tela de estoque
            tela_estoque = TelaEstoque(estoque_window)
            
            # Adicionar botão de voltar ao menu na tela de estoque
            self.add_back_button_to_estoque(tela_estoque)
            
            # Focar na nova janela
            estoque_window.focus_force()
            estoque_window.lift()
            
        except Exception as e:
            print(f"Erro ao abrir estoque completo: {e}")
            # Mostrar mensagem de erro para o usuário
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Erro")
            error_dialog.geometry("400x200")
            error_dialog.resizable(False, False)
            
            error_label = ctk.CTkLabel(
                error_dialog,
                text=f"Erro ao abrir módulo de estoque:\n{str(e)}",
                font=ctk.CTkFont(size=14),
                wraplength=350
            )
            error_label.pack(pady=40)
            
            ok_button = ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy,
                width=100
            )
            ok_button.pack(pady=10)
    
    def add_back_button_to_estoque(self, estoque_instance):
        """Adiciona botão 'Voltar ao Menu' no módulo de estoque"""
        # Criar frame para o botão voltar no topo
        back_frame = ctk.CTkFrame(
            estoque_instance,
            height=60,
            fg_color="#1a1a1a",
            corner_radius=0
        )
        back_frame.pack(fill="x", side="top", before=estoque_instance.winfo_children()[0])
        back_frame.pack_propagate(False)
        
        # Botão voltar ao menu
        btn_voltar = ctk.CTkButton(
            back_frame,
            text="⬅️ Voltar ao Menu Principal",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=220,
            fg_color="#1f538d",
            hover_color="#14375e",
            text_color="#ffffff",
            corner_radius=6,
            command=self.voltar_ao_menu,
            cursor="hand2"  # Cursor de mão para indicar clicável
        )
        btn_voltar.pack(side="left", padx=20, pady=10)
        
        # Adicionar efeito de feedback visual ao botão voltar
        def on_voltar_press(event):
            btn_voltar.configure(fg_color="#0a2a42")  # Cor mais escura quando pressionado
        
        def on_voltar_release(event):
            btn_voltar.configure(fg_color="#14375e")
        
        btn_voltar.bind("<Button-1>", on_voltar_press)
        btn_voltar.bind("<ButtonRelease-1>", on_voltar_release)
    
    def voltar_ao_menu(self):
        """Fecha a janela atual e retorna ao menu principal com transição suave"""
        try:
            # Obter a janela atual (que deve ser a janela de estoque)
            current_window = self.winfo_toplevel()
            
            # Desabilitar botão temporariamente
            for widget in current_window.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkFrame):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ctk.CTkButton) and "Voltar" in grandchild.cget("text"):
                                    grandchild.configure(state="disabled")
                                    break
            
            # Fechar a janela atual com um pequeno delay para suavidade
            def close_window():
                current_window.destroy()
            
            # Agendar fechamento após 200ms para dar feedback visual
            current_window.after(200, close_window)
            
        except Exception as e:
            print(f"Erro ao voltar ao menu: {e}")
            # Em caso de erro, apenas fechar a janela
            try:
                self.winfo_toplevel().destroy()
            except:
                pass

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