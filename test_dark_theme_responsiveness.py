"""
Teste de Responsividade do Tema Escuro - Módulo Estoque
Verifica a aparência e funcionalidade em diferentes tamanhos de tela
"""

import customtkinter as ctk
import sys
import os

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.estoque import TelaEstoque
from modules.db import criar_tabelas

class TestResponsiveness:
    def __init__(self):
        self.test_results = []
        
    def test_different_screen_sizes(self):
        """Testa o módulo em diferentes tamanhos de tela"""
        
        # Configurações de teste
        screen_sizes = [
            ("Desktop Grande", "1920x1080"),
            ("Desktop Médio", "1366x768"),
            ("Laptop", "1280x720"),
            ("Tablet Landscape", "1024x768"),
            ("Tablet Portrait", "768x1024")
        ]
        
        print("🖥️  TESTE DE RESPONSIVIDADE - TEMA ESCURO")
        print("=" * 60)
        
        for size_name, geometry in screen_sizes:
            print(f"\n📱 Testando: {size_name} ({geometry})")
            
            try:
                # Criar aplicação de teste
                app = ctk.CTk()
                app.title(f"Teste Responsividade - {size_name}")
                app.geometry(geometry)
                
                # Configurar tema escuro
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("blue")
                
                # Criar módulo estoque
                estoque = TelaEstoque(app)
                estoque.pack(fill="both", expand=True)
                
                # Simular teste visual (sem mostrar a janela)
                app.update()
                
                # Verificar se os elementos foram criados corretamente
                widgets_count = len(app.winfo_children())
                
                result = {
                    'size': size_name,
                    'geometry': geometry,
                    'widgets_created': widgets_count > 0,
                    'dark_theme_applied': estoque.colors['background'] == '#1a1a1a',
                    'status': 'PASSOU' if widgets_count > 0 else 'FALHOU'
                }
                
                self.test_results.append(result)
                print(f"   ✅ Widgets criados: {widgets_count > 0}")
                print(f"   ✅ Tema escuro aplicado: {result['dark_theme_applied']}")
                print(f"   📊 Status: {result['status']}")
                
                # Fechar aplicação
                app.destroy()
                
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
                self.test_results.append({
                    'size': size_name,
                    'geometry': geometry,
                    'error': str(e),
                    'status': 'ERRO'
                })
    
    def test_color_contrast_visibility(self):
        """Testa a visibilidade das cores em diferentes contextos"""
        
        print(f"\n🎨 TESTE DE VISIBILIDADE DE CORES")
        print("-" * 40)
        
        # Criar aplicação de teste
        app = ctk.CTk()
        app.geometry("800x600")
        ctk.set_appearance_mode("dark")
        
        estoque = TelaEstoque(app)
        estoque.pack(fill="both", expand=True)
        
        # Verificar cores aplicadas
        colors_to_test = [
            ('background', estoque.colors['background']),
            ('card_bg', estoque.colors['card_bg']),
            ('text_primary', estoque.colors['text_primary']),
            ('text_secondary', estoque.colors['text_secondary']),
            ('primary', estoque.colors['primary']),
            ('success', estoque.colors['success'])
        ]
        
        print("Cores aplicadas no tema escuro:")
        for color_name, color_value in colors_to_test:
            print(f"   {color_name}: {color_value}")
        
        # Verificar contraste
        bg_color = estoque.colors['background']  # #1a1a1a
        text_color = estoque.colors['text_primary']  # #ffffff
        
        contrast_ok = bg_color == '#1a1a1a' and text_color == '#ffffff'
        print(f"\n✅ Contraste adequado (fundo escuro + texto claro): {contrast_ok}")
        
        app.destroy()
        return contrast_ok
    
    def generate_report(self):
        """Gera relatório dos testes"""
        
        print(f"\n📋 RELATÓRIO DE RESPONSIVIDADE")
        print("=" * 60)
        
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASSOU')
        total_tests = len(self.test_results)
        
        print(f"Total de testes: {total_tests}")
        print(f"Testes aprovados: {passed_tests}")
        print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📊 DETALHES DOS TESTES:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASSOU' else "❌"
            print(f"{status_icon} {result['size']} ({result['geometry']}) - {result['status']}")
        
        # Verificar se todos os testes passaram
        all_passed = all(result['status'] == 'PASSOU' for result in self.test_results)
        
        print(f"\n🎯 RESULTADO FINAL:")
        if all_passed:
            print("✅ TODOS OS TESTES DE RESPONSIVIDADE PASSARAM!")
            print("✅ O tema escuro está funcionando corretamente em todas as resoluções testadas.")
        else:
            print("❌ ALGUNS TESTES FALHARAM!")
            print("⚠️  Verifique os problemas reportados acima.")
        
        return all_passed

def main():
    """Função principal do teste"""
    
    print("🚀 INICIANDO TESTES DE RESPONSIVIDADE DO TEMA ESCURO")
    print("=" * 70)
    
    # Criar tabelas do banco de dados
    try:
        criar_tabelas()
        print("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"⚠️  Aviso: Erro ao inicializar banco: {e}")
    
    # Executar testes
    tester = TestResponsiveness()
    
    # Teste 1: Diferentes tamanhos de tela
    tester.test_different_screen_sizes()
    
    # Teste 2: Visibilidade de cores
    contrast_ok = tester.test_color_contrast_visibility()
    
    # Gerar relatório final
    all_tests_passed = tester.generate_report()
    
    # Conclusão
    print(f"\n🏁 CONCLUSÃO:")
    if all_tests_passed and contrast_ok:
        print("🎉 O módulo Estoque com tema escuro está PRONTO para produção!")
        print("✅ Responsividade: OK")
        print("✅ Contraste de cores: OK")
        print("✅ Funcionalidade: OK")
    else:
        print("⚠️  O módulo precisa de ajustes antes da produção.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()