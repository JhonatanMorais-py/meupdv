#!/usr/bin/env python3
"""
Teste de Conformidade WCAG AA - Contraste de Cores
Verifica se as cores do módulo de estoque atendem aos requisitos de acessibilidade
"""

def hex_to_rgb(hex_color):
    """Converte cor hexadecimal para RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """Calcula a luminância relativa de uma cor RGB"""
    def gamma_correct(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return pow((c + 0.055) / 1.055, 2.4)
    
    r, g, b = rgb
    return 0.2126 * gamma_correct(r) + 0.7152 * gamma_correct(g) + 0.0722 * gamma_correct(b)

def contrast_ratio(color1, color2):
    """Calcula a razão de contraste entre duas cores"""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))
    
    # Garante que a cor mais clara seja o numerador
    if lum1 > lum2:
        return (lum1 + 0.05) / (lum2 + 0.05)
    else:
        return (lum2 + 0.05) / (lum1 + 0.05)

def test_wcag_compliance():
    """Testa a conformidade WCAG AA das cores corporativas"""
    
    # Paleta de cores corporativa
    colors = {
        'primary': '#1f538d',           # Azul corporativo principal
        'primary_hover': '#14375e',     # Azul hover
        'secondary': '#2b2b2b',         # Cinza escuro secundário
        'background': '#f8f9fa',        # Fundo claro
        'card_bg': '#ffffff',           # Fundo dos cards
        'text_primary': '#2b2b2b',      # Texto principal escuro
        'text_secondary': '#495057',    # Texto secundário (ajustado para WCAG AA)
        'text_light': '#ffffff',        # Texto claro
        'success': '#1e7e34',           # Verde para sucesso (ajustado para WCAG AA)
        'success_hover': '#155724',     # Verde hover (mais escuro)
        'warning': '#ffc107',           # Amarelo para avisos
        'warning_hover': '#e0a800',     # Amarelo hover
        'danger': '#dc3545',            # Vermelho para perigo
        'danger_hover': '#c82333',      # Vermelho hover
        'neutral': '#6c757d',           # Cinza neutro
        'neutral_hover': '#5a6268',     # Cinza neutro hover
        'border': '#dee2e6',            # Bordas
        'input_bg': '#ffffff',          # Fundo dos inputs
        'accent': '#0078d4'             # Azul de destaque
    }
    
    # Combinações críticas para teste WCAG AA (mínimo 4.5:1 para texto normal)
    critical_combinations = [
        ('text_primary', 'background', 'Texto principal em fundo claro'),
        ('text_primary', 'card_bg', 'Texto principal em cards'),
        ('text_secondary', 'background', 'Texto secundário em fundo claro'),
        ('text_secondary', 'card_bg', 'Texto secundário em cards'),
        ('text_light', 'primary', 'Texto claro em botão primário'),
        ('text_light', 'success', 'Texto claro em botão de sucesso'),
        ('text_light', 'danger', 'Texto claro em botão de perigo'),
        ('text_light', 'neutral', 'Texto claro em botão neutro'),
        ('text_primary', 'warning', 'Texto escuro em botão de aviso'),
        ('text_light', 'accent', 'Texto claro em botão de destaque'),
    ]
    
    print("=" * 70)
    print("TESTE DE CONFORMIDADE WCAG AA - CONTRASTE DE CORES")
    print("=" * 70)
    print("Requisito mínimo: 4.5:1 para texto normal")
    print("Requisito mínimo: 3:1 para texto grande (18pt+ ou 14pt+ negrito)")
    print("=" * 70)
    
    all_passed = True
    
    for text_color, bg_color, description in critical_combinations:
        ratio = contrast_ratio(colors[text_color], colors[bg_color])
        
        # WCAG AA: 4.5:1 para texto normal, 3:1 para texto grande
        normal_pass = ratio >= 4.5
        large_pass = ratio >= 3.0
        
        status_normal = "✅ APROVADO" if normal_pass else "❌ REPROVADO"
        status_large = "✅ APROVADO" if large_pass else "❌ REPROVADO"
        
        print(f"\n{description}:")
        print(f"  Cores: {colors[text_color]} sobre {colors[bg_color]}")
        print(f"  Contraste: {ratio:.2f}:1")
        print(f"  Texto normal: {status_normal}")
        print(f"  Texto grande: {status_large}")
        
        if not normal_pass:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("🎉 RESULTADO: TODAS AS COMBINAÇÕES APROVADAS!")
        print("✅ O módulo de estoque está em conformidade com WCAG AA")
    else:
        print("⚠️  RESULTADO: ALGUMAS COMBINAÇÕES REPROVADAS")
        print("❌ Ajustes necessários para conformidade total com WCAG AA")
    
    print("=" * 70)
    
    # Teste adicional: Contraste entre cores de estado
    print("\nTESTE ADICIONAL: CONTRASTE ENTRE CORES DE ESTADO")
    print("-" * 50)
    
    state_colors = [
        ('success', 'Verde de sucesso'),
        ('warning', 'Amarelo de aviso'),
        ('danger', 'Vermelho de perigo'),
        ('primary', 'Azul primário'),
        ('accent', 'Azul de destaque')
    ]
    
    for color_key, description in state_colors:
        bg_ratio = contrast_ratio(colors[color_key], colors['background'])
        card_ratio = contrast_ratio(colors[color_key], colors['card_bg'])
        
        print(f"\n{description} ({colors[color_key]}):")
        print(f"  Sobre fundo claro: {bg_ratio:.2f}:1")
        print(f"  Sobre cards: {card_ratio:.2f}:1")
    
    return all_passed

if __name__ == "__main__":
    test_wcag_compliance()