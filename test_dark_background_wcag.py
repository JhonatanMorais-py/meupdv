#!/usr/bin/env python3
"""
Teste WCAG AA - Fundo Escuro para Módulo de Estoque
Testa diferentes opções de fundo escuro e verifica conformidade com WCAG AA
"""

def hex_to_rgb(hex_color):
    """Converte cor hexadecimal para RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_relative_luminance(rgb):
    """Calcula a luminância relativa de uma cor RGB"""
    def normalize_component(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = rgb
    r_norm = normalize_component(r)
    g_norm = normalize_component(g)
    b_norm = normalize_component(b)
    
    return 0.2126 * r_norm + 0.7152 * g_norm + 0.0722 * b_norm

def calculate_contrast_ratio(color1, color2):
    """Calcula a razão de contraste entre duas cores"""
    lum1 = get_relative_luminance(hex_to_rgb(color1))
    lum2 = get_relative_luminance(hex_to_rgb(color2))
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)

def test_wcag_compliance(bg_color, text_color, min_ratio=4.5):
    """Testa se uma combinação de cores atende aos padrões WCAG AA"""
    ratio = calculate_contrast_ratio(bg_color, text_color)
    passes = ratio >= min_ratio
    return ratio, passes

def main():
    """Testa diferentes opções de fundo escuro para o módulo de estoque"""
    
    print("=" * 80)
    print("TESTE WCAG AA - OPÇÕES DE FUNDO ESCURO PARA MÓDULO DE ESTOQUE")
    print("=" * 80)
    
    # Cores de texto atuais do módulo
    text_colors = {
        'text_primary': '#2b2b2b',      # Texto principal escuro
        'text_secondary': '#495057',    # Texto secundário
        'text_light': '#ffffff',        # Texto claro
    }
    
    # Opções de fundo escuro baseadas na paleta do dashboard
    dark_background_options = {
        'content_bg_dashboard': '#2b2b2b',      # Fundo do conteúdo do dashboard
        'sidebar_bg_dashboard': '#1a1a1a',      # Fundo da sidebar do dashboard
        'secondary_dashboard': '#2b2b2b',       # Cor secundária do dashboard
        'darker_gray': '#343a40',               # Cinza mais escuro
        'charcoal': '#36393f',                  # Carvão (Discord-like)
        'dark_slate': '#2f3349',               # Ardósia escura
        'navy_dark': '#1e2124',                # Azul marinho escuro
        'custom_dark_1': '#212529',            # Bootstrap dark
        'custom_dark_2': '#1c1e21',            # Quase preto
        'custom_dark_3': '#25282c'             # Cinza escuro médio
    }
    
    print("\n🎨 TESTANDO OPÇÕES DE FUNDO ESCURO:")
    print("-" * 80)
    
    best_options = []
    
    for bg_name, bg_color in dark_background_options.items():
        print(f"\n📋 FUNDO: {bg_name.upper()} ({bg_color})")
        print("-" * 50)
        
        all_pass = True
        bg_results = {'name': bg_name, 'color': bg_color, 'results': []}
        
        # Testar com texto claro (branco) - principal para fundos escuros
        ratio, passes = test_wcag_compliance(bg_color, text_colors['text_light'])
        status = "✅ PASSA" if passes else "❌ FALHA"
        print(f"Texto claro (#ffffff):     Contraste {ratio:.2f}:1 | {status}")
        bg_results['results'].append({
            'text': 'text_light',
            'ratio': ratio,
            'passes': passes
        })
        if not passes:
            all_pass = False
        
        # Testar com texto primário (escuro) - para verificar se ainda funciona
        ratio, passes = test_wcag_compliance(bg_color, text_colors['text_primary'])
        status = "✅ PASSA" if passes else "❌ FALHA"
        print(f"Texto primário (#2b2b2b):  Contraste {ratio:.2f}:1 | {status}")
        bg_results['results'].append({
            'text': 'text_primary',
            'ratio': ratio,
            'passes': passes
        })
        
        # Testar com texto secundário
        ratio, passes = test_wcag_compliance(bg_color, text_colors['text_secondary'])
        status = "✅ PASSA" if passes else "❌ FALHA"
        print(f"Texto secundário (#495057): Contraste {ratio:.2f}:1 | {status}")
        bg_results['results'].append({
            'text': 'text_secondary',
            'ratio': ratio,
            'passes': passes
        })
        
        # Verificar se pelo menos o texto claro passa (principal para fundos escuros)
        text_light_passes = bg_results['results'][0]['passes']
        
        if text_light_passes:
            best_options.append(bg_results)
            print(f"🎯 RESULTADO: ADEQUADO (texto claro funciona)")
        else:
            print(f"⚠️  RESULTADO: NÃO ADEQUADO (texto claro não passa)")
    
    # Mostrar melhores opções
    print("\n" + "=" * 80)
    print("🏆 MELHORES OPÇÕES DE FUNDO ESCURO")
    print("=" * 80)
    
    if best_options:
        # Ordenar por melhor contraste com texto claro
        best_options.sort(key=lambda x: x['results'][0]['ratio'], reverse=True)
        
        print("\n🥇 TOP 3 RECOMENDAÇÕES:")
        print("-" * 50)
        
        for i, option in enumerate(best_options[:3], 1):
            text_light_ratio = option['results'][0]['ratio']
            print(f"{i}. {option['name']} ({option['color']})")
            print(f"   Contraste com texto claro: {text_light_ratio:.2f}:1")
            
            # Verificar compatibilidade com dashboard
            if option['color'] in ['#2b2b2b', '#1a1a1a']:
                print(f"   ✅ Compatível com paleta do dashboard")
            else:
                print(f"   ⚠️  Nova cor (não está na paleta atual)")
            print()
        
        # Recomendação final
        recommended = best_options[0]
        print("🎯 RECOMENDAÇÃO FINAL:")
        print("-" * 50)
        print(f"Cor: {recommended['name']} ({recommended['color']})")
        print(f"Contraste com texto claro: {recommended['results'][0]['ratio']:.2f}:1")
        
        if recommended['color'] == '#2b2b2b':
            print("✅ Esta cor já está na paleta do dashboard como 'content_bg'")
            print("✅ Garantirá consistência visual com outros módulos")
        
    else:
        print("❌ Nenhuma opção de fundo escuro atende aos critérios WCAG AA")
    
    print("\n" + "=" * 80)
    print("📋 RESUMO DAS DIRETRIZES:")
    print("=" * 80)
    print("• WCAG AA exige contraste mínimo de 4.5:1 para texto normal")
    print("• WCAG AA exige contraste mínimo de 3:1 para texto grande")
    print("• Fundos escuros devem usar texto claro (#ffffff) como padrão")
    print("• Manter consistência com a paleta do dashboard")
    print("• Testar em diferentes dispositivos e condições de iluminação")
    print("=" * 80)

if __name__ == "__main__":
    main()