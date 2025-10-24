import sqlite3

def verificar_estrutura_db():
    try:
        conn = sqlite3.connect('pdv.db')
        cursor = conn.cursor()
        
        # Verificar tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        print("Tabelas encontradas:", tabelas)
        
        # Verificar estrutura da tabela vendas
        try:
            cursor.execute("PRAGMA table_info(vendas)")
            estrutura_vendas = cursor.fetchall()
            print("\nEstrutura da tabela vendas:")
            for coluna in estrutura_vendas:
                print(f"  {coluna}")
        except Exception as e:
            print(f"Erro ao verificar tabela vendas: {e}")
        
        # Verificar estrutura da tabela produtos
        try:
            cursor.execute("PRAGMA table_info(produtos)")
            estrutura_produtos = cursor.fetchall()
            print("\nEstrutura da tabela produtos:")
            for coluna in estrutura_produtos:
                print(f"  {coluna}")
        except Exception as e:
            print(f"Erro ao verificar tabela produtos: {e}")
        
        # Verificar dados de exemplo
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas")
            count_vendas = cursor.fetchone()[0]
            print(f"\nTotal de vendas: {count_vendas}")
            
            cursor.execute("SELECT COUNT(*) FROM produtos")
            count_produtos = cursor.fetchone()[0]
            print(f"Total de produtos: {count_produtos}")
        except Exception as e:
            print(f"Erro ao contar registros: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar com o banco: {e}")

if __name__ == "__main__":
    verificar_estrutura_db()