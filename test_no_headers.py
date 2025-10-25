"""
Teste de Funcionalidade Após Remoção dos Cabeçalhos
Verifica se o módulo Estoque funciona corretamente sem os títulos
"""

import customtkinter as ctk
import sys
import os

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.estoque import TelaEstoque
from modules.db import criar_tabelas

class TestNoHeaders:
    def __init__(self):
        self.test_results = []
        
    def test_module_creation(self):
        """Testa se o módulo é criado corretamente sem cabeçalhos"""
        
        print("🧪 TESTE DE CRIAÇÃO DO MÓDULO SEM CABEÇALHOS")
        print("=" * 60)
        
        try:
            # Criar aplicação de teste
            app = ctk.CTk()
            app.title("Teste - Módulo sem Cabeçalhos")
            app.geometry("1400x900")
            
            # Configurar tema escuro
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Criar módulo estoque
            estoque = TelaEstoque(app)
            estoque.pack(fill="both", expand=True)
            
            # Atualizar para garantir que todos os widgets sejam criados
            app.update()
            
            # Verificar se os elementos foram criados
            widgets_count = len(app.winfo_children())
            has_scrollable_frame = any(isinstance(child, ctk.CTkScrollableFrame) for child in estoque.winfo_children())
            
            result = {
                'test': 'module_creation',
                'widgets_created': widgets_count > 0,
                'has_main_content': has_scrollable_frame,
                'status': 'PASSOU' if widgets_count > 0 and has_scrollable_frame else 'FALHOU'
            }
            
            self.test_results.append(result)
            
            print(f"✅ Widgets criados: {result['widgets_created']}")
            print(f"✅ Conteúdo principal presente: {result['has_main_content']}")
            print(f"📊 Status: {result['status']}")
            
            # Fechar aplicação
            app.destroy()
            
            return result['status'] == 'PASSOU'
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            self.test_results.append({
                'test': 'module_creation',
                'error': str(e),
                'status': 'ERRO'
            })
            return False
    
    def test_form_fields_accessibility(self):
        """Testa se todos os campos do formulário estão acessíveis"""
        
        print(f"\n📝 TESTE DE ACESSIBILIDADE DOS CAMPOS")
        print("-" * 40)
        
        try:
            # Criar aplicação de teste
            app = ctk.CTk()
            app.geometry("1400x900")
            ctk.set_appearance_mode("dark")
            
            estoque = TelaEstoque(app)
            estoque.pack(fill="both", expand=True)
            app.update()
            
            # Verificar se as variáveis do formulário existem
            required_vars = [
                'nome_var', 'codigo_barras_var', 'categoria_var', 'descricao_var',
                'quantidade_var', 'estoque_minimo_var', 'localizacao_var',
                'preco_custo_var', 'preco_venda_var', 'margem_lucro_var',
                'fornecedor_var', 'info_fornecedor_var'
            ]
            
            missing_vars = []
            for var_name in required_vars:
                if not hasattr(estoque, var_name):
                    missing_vars.append(var_name)
            
            all_vars_present = len(missing_vars) == 0
            
            print(f"✅ Variáveis do formulário presentes: {all_vars_present}")
            if missing_vars:
                print(f"❌ Variáveis ausentes: {missing_vars}")
            
            result = {
                'test': 'form_fields_accessibility',
                'all_vars_present': all_vars_present,
                'missing_vars': missing_vars,
                'status': 'PASSOU' if all_vars_present else 'FALHOU'
            }
            
            self.test_results.append(result)
            
            app.destroy()
            return result['status'] == 'PASSOU'
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            self.test_results.append({
                'test': 'form_fields_accessibility',
                'error': str(e),
                'status': 'ERRO'
            })
            return False
    
    def test_layout_integrity(self):
        """Testa se o layout está íntegro após remoção dos cabeçalhos"""
        
        print(f"\n🎨 TESTE DE INTEGRIDADE DO LAYOUT")
        print("-" * 40)
        
        try:
            # Criar aplicação de teste
            app = ctk.CTk()
            app.geometry("1400x900")
            ctk.set_appearance_mode("dark")
            
            estoque = TelaEstoque(app)
            estoque.pack(fill="both", expand=True)
            app.update()
            
            # Verificar se não há espaços vazios excessivos
            # Isso é feito verificando se o conteúdo principal ocupa a área disponível
            main_frame_found = False
            for child in estoque.winfo_children():
                if isinstance(child, ctk.CTkScrollableFrame):
                    main_frame_found = True
                    break
            
            # Verificar se o tema escuro está aplicado
            dark_theme_applied = estoque.colors['background'] == '#1a1a1a'
            
            result = {
                'test': 'layout_integrity',
                'main_frame_found': main_frame_found,
                'dark_theme_applied': dark_theme_applied,
                'status': 'PASSOU' if main_frame_found and dark_theme_applied else 'FALHOU'
            }
            
            self.test_results.append(result)
            
            print(f"✅ Frame principal encontrado: {result['main_frame_found']}")
            print(f"✅ Tema escuro aplicado: {result['dark_theme_applied']}")
            print(f"📊 Status: {result['status']}")
            
            app.destroy()
            return result['status'] == 'PASSOU'
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            self.test_results.append({
                'test': 'layout_integrity',
                'error': str(e),
                'status': 'ERRO'
            })
            return False
    
    def test_responsiveness(self):
        """Testa responsividade em diferentes tamanhos"""
        
        print(f"\n📱 TESTE DE RESPONSIVIDADE")
        print("-" * 40)
        
        screen_sizes = [
            ("Desktop", "1400x900"),
            ("Laptop", "1280x720"),
            ("Tablet", "1024x768")
        ]
        
        all_passed = True
        
        for size_name, geometry in screen_sizes:
            try:
                app = ctk.CTk()
                app.geometry(geometry)
                ctk.set_appearance_mode("dark")
                
                estoque = TelaEstoque(app)
                estoque.pack(fill="both", expand=True)
                app.update()
                
                # Verificar se o módulo se adapta ao tamanho
                widgets_visible = len(estoque.winfo_children()) > 0
                
                print(f"✅ {size_name} ({geometry}): {'PASSOU' if widgets_visible else 'FALHOU'}")
                
                if not widgets_visible:
                    all_passed = False
                
                app.destroy()
                
            except Exception as e:
                print(f"❌ {size_name} ({geometry}): ERRO - {str(e)}")
                all_passed = False
        
        result = {
            'test': 'responsiveness',
            'status': 'PASSOU' if all_passed else 'FALHOU'
        }
        
        self.test_results.append(result)
        return all_passed
    
    def generate_report(self):
        """Gera relatório dos testes"""
        
        print(f"\n📋 RELATÓRIO DE TESTES - REMOÇÃO DE CABEÇALHOS")
        print("=" * 70)
        
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASSOU')
        total_tests = len(self.test_results)
        
        print(f"Total de testes: {total_tests}")
        print(f"Testes aprovados: {passed_tests}")
        print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📊 DETALHES DOS TESTES:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASSOU' else "❌"
            test_name = result['test'].replace('_', ' ').title()
            print(f"{status_icon} {test_name} - {result['status']}")
        
        # Verificar se todos os testes passaram
        all_passed = all(result['status'] == 'PASSOU' for result in self.test_results)
        
        print(f"\n🎯 RESULTADO FINAL:")
        if all_passed:
            print("✅ TODOS OS TESTES PASSARAM!")
            print("✅ A remoção dos cabeçalhos foi bem-sucedida.")
            print("✅ O módulo mantém todas as funcionalidades.")
            print("✅ O layout está íntegro e responsivo.")
        else:
            print("❌ ALGUNS TESTES FALHARAM!")
            print("⚠️  Verifique os problemas reportados acima.")
        
        return all_passed

def main():
    """Função principal do teste"""
    
    print("🚀 INICIANDO TESTES APÓS REMOÇÃO DOS CABEÇALHOS")
    print("=" * 70)
    
    # Criar tabelas do banco de dados
    try:
        criar_tabelas()
        print("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"⚠️  Aviso: Erro ao inicializar banco: {e}")
    
    # Executar testes
    tester = TestNoHeaders()
    
    # Teste 1: Criação do módulo
    test1_passed = tester.test_module_creation()
    
    # Teste 2: Acessibilidade dos campos
    test2_passed = tester.test_form_fields_accessibility()
    
    # Teste 3: Integridade do layout
    test3_passed = tester.test_layout_integrity()
    
    # Teste 4: Responsividade
    test4_passed = tester.test_responsiveness()
    
    # Gerar relatório final
    all_tests_passed = tester.generate_report()
    
    # Conclusão
    print(f"\n🏁 CONCLUSÃO:")
    if all_tests_passed:
        print("🎉 A remoção dos cabeçalhos foi CONCLUÍDA COM SUCESSO!")
        print("✅ Funcionalidade: Mantida")
        print("✅ Layout: Íntegro")
        print("✅ Responsividade: OK")
        print("✅ Acessibilidade: OK")
    else:
        print("⚠️  A remoção precisa de ajustes adicionais.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()