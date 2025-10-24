import sqlite3


def conectar():
    return sqlite3.connect("database/db.sqlite3")


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de fornecedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            contato TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            informacoes_adicionais TEXT
        )
    """)

    # Tabela de produtos completa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT NOT NULL,
            codigo_barras TEXT UNIQUE,
            quantidade INTEGER DEFAULT 0,
            estoque_minimo INTEGER DEFAULT 0,
            localizacao TEXT,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            margem_lucro REAL,
            fornecedor_id INTEGER,
            imagem_path TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)

    # Usuário padrão
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (id, nome, senha) VALUES (1, 'admin', '1234')")
    
    # Fornecedores padrão
    cursor.execute("""
        INSERT OR IGNORE INTO fornecedores (id, nome, contato, telefone, email) 
        VALUES 
        (1, 'Fornecedor Geral', 'Contato Geral', '(11) 99999-9999', 'contato@fornecedor.com'),
        (2, 'Distribuidora ABC', 'João Silva', '(11) 88888-8888', 'joao@abc.com'),
        (3, 'Atacado XYZ', 'Maria Santos', '(11) 77777-7777', 'maria@xyz.com')
    """)
    
    conn.commit()
    conn.close()
