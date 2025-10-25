#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Navegação - Verificação após remoção de cabeçalhos
Verifica se a navegação entre seções do sistema não foi afetada
"""

import customtkinter as ctk
import sys
import os
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_navigation():
    """Testa a navegação entre seções do sistema"""
    print("🧭 TESTE DE NAVEGAÇÃO - REMOÇÃO DE CABEÇALHOS")
    print("=" * 60)
    
    # Configurar tema escuro
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar aplicação de teste
    app = ctk.CTk()
    app.title("Teste de Navegação")
    app.geometry("1200x800")
    app.withdraw()  # Ocultar janela durante o teste
    
    test_results = {
        "estoque_module": False,
        "dashboard_navigation": False,
        "module_switching": False,
        "form_accessibility": False
    }
    
    try:
        print("\n📦 TESTE 1: Carregamento do Módulo Estoque")
        print("-" * 40)
        
        # Importar e criar módulo de estoque
        from modules.estoque import TelaEstoque
        estoque = TelaEstoque(app)
        estoque.pack(fill="both", expand=True)
        
        # Verificar se o módulo foi criado corretamente
        if hasattr(estoque, 'main_frame'):
            print("✅ Módulo de estoque carregado com sucesso")
            test_results["estoque_module"] = True
        else:
            print("❌ Falha no carregamento do módulo de estoque")
        
        print("\n🏠 TESTE 2: Navegação do Dashboard")
        print("-" * 40)
        
        # Testar importação do dashboard
        try:
            from ui.dashbord import TelaDashboard
            dashboard = TelaDashboard()
            dashboard.withdraw()  # Ocultar janela
            print("✅ Dashboard importado com sucesso")
            test_results["dashboard_navigation"] = True
            dashboard.destroy()
        except Exception as e:
            print(f"❌ Erro na importação do dashboard: {e}")
        
        print("\n🔄 TESTE 3: Alternância entre Módulos")
        print("-" * 40)
        
        # Simular alternância entre módulos
        try:
            # Remover módulo atual
            estoque.pack_forget()
            
            # Recriar módulo
            estoque2 = TelaEstoque(app)
            estoque2.pack(fill="both", expand=True)
            
            print("✅ Alternância entre módulos funcionando")
            test_results["module_switching"] = True
        except Exception as e:
            print(f"❌ Erro na alternância de módulos: {e}")
        
        print("\n📝 TESTE 4: Acessibilidade dos Formulários")
        print("-" * 40)
        
        # Verificar se os campos do formulário estão acessíveis
        form_fields = [
            'nome_var', 'codigo_barras_var', 'categoria_var',
            'quantidade_var', 'preco_custo_var', 'preco_venda_var'
        ]
        
        accessible_fields = 0
        for field in form_fields:
            if hasattr(estoque2, field):
                accessible_fields += 1
        
        if accessible_fields == len(form_fields):
            print("✅ Todos os campos do formulário estão acessíveis")
            test_results["form_accessibility"] = True
        else:
            print(f"❌ Apenas {accessible_fields}/{len(form_fields)} campos acessíveis")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
    
    finally:
        app.destroy()
    
    # Gerar relatório
    print("\n📋 RELATÓRIO DE NAVEGAÇÃO")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"Total de testes: {total_tests}")
    print(f"Testes aprovados: {passed_tests}")
    print(f"Taxa de sucesso: {success_rate:.1f}%")
    
    print("\n📊 DETALHES DOS TESTES:")
    for test_name, result in test_results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        test_display = test_name.replace("_", " ").title()
        print(f"{status} {test_display}")
    
    print("\n🎯 RESULTADO FINAL:")
    if success_rate == 100:
        print("✅ TODOS OS TESTES DE NAVEGAÇÃO PASSARAM!")
        print("🎉 A navegação está funcionando perfeitamente.")
    elif success_rate >= 75:
        print("⚠️  MAIORIA DOS TESTES PASSOU!")
        print("🔧 Pequenos ajustes podem ser necessários.")
    else:
        print("❌ VÁRIOS TESTES FALHARAM!")
        print("⚠️  Verificação adicional necessária.")
    
    print(f"\n🕒 Teste executado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    return success_rate == 100

if __name__ == "__main__":
    test_navigation()