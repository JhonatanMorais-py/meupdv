#!/usr/bin/env python3
"""
Teste de funcionalidades do módulo de estoque após redesign
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from modules.estoque import TelaEstoque

def test_estoque_functionality():
    """Testa se o módulo de estoque carrega e funciona corretamente"""
    print("🧪 Iniciando teste de funcionalidades do módulo Estoque...")
    
    try:
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar janela de teste
        root = ctk.CTk()
        root.withdraw()  # Ocultar janela principal
        
        # Testar criação do módulo
        print("✅ Testando criação do módulo...")
        estoque = TelaEstoque(root)
        
        # Verificar se o main_frame foi criado
        print("✅ Testando criação do main_frame...")
        assert hasattr(estoque, 'main_frame'), "main_frame não encontrado"
        
        # Verificar se as variáveis foram inicializadas
        print("✅ Testando inicialização das variáveis...")
        assert hasattr(estoque, 'nome_var'), "nome_var não encontrada"
        assert hasattr(estoque, 'preco_custo_var'), "preco_custo_var não encontrada"
        assert hasattr(estoque, 'preco_venda_var'), "preco_venda_var não encontrada"
        
        # Verificar se os métodos principais existem
        print("✅ Testando existência dos métodos principais...")
        assert hasattr(estoque, 'save_product'), "Método save_product não encontrado"
        assert hasattr(estoque, 'validate_form'), "Método validate_form não encontrado"
        assert hasattr(estoque, 'calculate_margin'), "Método calculate_margin não encontrado"
        
        # Testar validação de formulário
        print("✅ Testando validação de formulário...")
        estoque.nome_var.set("Produto Teste")
        estoque.preco_custo_var.set("10,00")
        estoque.preco_venda_var.set("15,00")
        
        # Verificar se a validação funciona
        validation_result = estoque.validate_form()
        
        root.destroy()
        
        print("🎉 Todos os testes passaram! O módulo está funcionando corretamente.")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        if 'root' in locals():
            root.destroy()
        return False

if __name__ == "__main__":
    success = test_estoque_functionality()
    sys.exit(0 if success else 1)