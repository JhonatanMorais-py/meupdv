"""
Script para testar a responsividade do dashboard em diferentes tamanhos de tela
"""
import sys
sys.path.append('.')
from ui.dashbord import TelaDashboard
import customtkinter as ctk
import time

def test_different_sizes():
    """Testa o dashboard em diferentes tamanhos de tela"""
    
    # Tamanhos de tela para testar
    screen_sizes = [
        (1024, 768),   # Tablet landscape
        (1366, 768),   # Laptop pequeno
        (1920, 1080),  # Full HD
        (800, 600),    # Tela pequena
        (1440, 900),   # MacBook Air
    ]
    
    for width, height in screen_sizes:
        print(f"\nTestando resolução: {width}x{height}")
        
        # Criar instância do dashboard
        app = TelaDashboard('Usuário Teste')
        
        # Definir tamanho da janela
        app.geometry(f"{width}x{height}")
        
        # Centralizar na tela
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        app.geometry(f"{width}x{height}+{x}+{y}")
        
        # Atualizar título para mostrar resolução atual
        app.title(f"Dashboard PDV - {width}x{height}")
        
        print(f"Dashboard aberto em {width}x{height}")
        print("Feche a janela para testar o próximo tamanho...")
        
        # Executar o mainloop
        app.mainloop()
        
        print(f"Teste concluído para {width}x{height}")

if __name__ == "__main__":
    print("=== Teste de Responsividade do Dashboard ===")
    print("Este script testará o dashboard em diferentes resoluções.")
    print("Feche cada janela para prosseguir para o próximo teste.\n")
    
    test_different_sizes()
    
    print("\n=== Todos os testes concluídos! ===")