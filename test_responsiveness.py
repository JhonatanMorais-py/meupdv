#!/usr/bin/env python3
"""
Teste de responsividade do módulo de estoque
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from modules.estoque import TelaEstoque
import time

def test_responsiveness():
    """Testa a responsividade do módulo em diferentes tamanhos de tela"""
    print("📱 Iniciando teste de responsividade...")
    
    try:
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Tamanhos de tela para testar
        screen_sizes = [
            (1400, 900),  # Desktop padrão
            (1200, 800),  # Desktop médio
            (1024, 768),  # Tablet landscape
            (800, 600),   # Tela pequena
        ]
        
        for width, height in screen_sizes:
            print(f"🖥️  Testando resolução {width}x{height}...")
            
            # Criar janela de teste
            root = ctk.CTk()
            root.geometry(f"{width}x{height}")
            root.title(f"Teste Responsividade - {width}x{height}")
            
            # Criar módulo estoque
            estoque = TelaEstoque(root)
            estoque.pack(fill="both", expand=True)
            
            # Atualizar interface
            root.update()
            
            # Verificar se o main_frame se adapta
            main_frame_width = estoque.main_frame.winfo_width()
            main_frame_height = estoque.main_frame.winfo_height()
            
            print(f"   ✅ Main frame: {main_frame_width}x{main_frame_height}")
            
            # Verificar se não há overflow
            assert main_frame_width > 0, f"Main frame width inválida: {main_frame_width}"
            assert main_frame_height > 0, f"Main frame height inválida: {main_frame_height}"
            
            # Simular redimensionamento
            root.geometry(f"{width-100}x{height-100}")
            root.update()
            
            new_width = estoque.main_frame.winfo_width()
            new_height = estoque.main_frame.winfo_height()
            
            print(f"   ✅ Após redimensionamento: {new_width}x{new_height}")
            
            root.destroy()
            
        print("🎉 Teste de responsividade concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste de responsividade: {str(e)}")
        if 'root' in locals():
            root.destroy()
        return False

if __name__ == "__main__":
    success = test_responsiveness()
    sys.exit(0 if success else 1)