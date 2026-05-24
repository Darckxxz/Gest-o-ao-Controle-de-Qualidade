import sqlite3
import os

# Caminho padrão do banco de dados SQLite (na raiz do projeto)
_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'taskflow.db')


def set_database_path(path):
    """Define um caminho personalizado para o banco de dados (usado em testes)."""
    global _DB_PATH
    _DB_PATH = path


def get_connection():
    """Abre e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(_DB_PATH)
    # Permite acessar colunas pelo nome em vez de índice
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Cria as tabelas do banco de dados caso ainda não existam."""
    conn = get_connection()

    # Tabela principal: armazena todas as tarefas do sistema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT    NOT NULL,
            descricao    TEXT    DEFAULT '',
            status       TEXT    DEFAULT 'pendente',
            prioridade   TEXT    DEFAULT 'media',
            criado_em    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de usuários - adicionada na mudança de escopo (Sprint 2)
    # Justificativa: cliente solicitou controle de acesso por colaborador
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            email     TEXT UNIQUE NOT NULL,
            senha     TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
