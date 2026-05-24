from flask import Blueprint, request, jsonify
from src.database import get_connection

# Módulo de autenticação adicionado na mudança de escopo (Sprint 2)
# Motivação: controlar quais colaboradores podem modificar tarefas críticas
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    """Registra um novo usuário no sistema."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados ausentes ou inválidos.'}), 400

    nome = dados.get('nome', '').strip()
    email = dados.get('email', '').strip()
    senha = dados.get('senha', '')

    # Validação básica dos campos obrigatórios
    if not nome or not email or not senha:
        return jsonify({'erro': 'Nome, email e senha são obrigatórios.'}), 422

    conn = get_connection()
    try:
        conn.execute(
            'INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)',
            (nome, email, senha)
        )
        conn.commit()
        return jsonify({'mensagem': 'Usuário registrado com sucesso.'}), 201
    except Exception:
        # E-mail duplicado viola a restrição UNIQUE da tabela
        return jsonify({'erro': 'E-mail já cadastrado.'}), 409
    finally:
        conn.close()


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Autentica um usuário com e-mail e senha."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados ausentes ou inválidos.'}), 400

    email = dados.get('email', '').strip()
    senha = dados.get('senha', '')

    if not email or not senha:
        return jsonify({'erro': 'E-mail e senha são obrigatórios.'}), 422

    conn = get_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND senha = ?', (email, senha)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({'erro': 'Credenciais inválidas.'}), 401

    return jsonify({
        'mensagem': 'Login realizado com sucesso.',
        'usuario': {
            'id': user['id'],
            'nome': user['nome'],
            'email': user['email'],
        }
    }), 200
