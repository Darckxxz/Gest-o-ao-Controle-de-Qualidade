from flask import Blueprint, request, jsonify
from src.models.task import Task

# Agrupa todas as rotas relacionadas a tarefas
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
def listar_tarefas():
    """Retorna a lista completa de tarefas cadastradas."""
    tarefas = Task.buscar_todos()
    return jsonify([t.to_dict() for t in tarefas]), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def buscar_tarefa(task_id):
    """Retorna uma tarefa específica pelo seu ID."""
    tarefa = Task.buscar_por_id(task_id)
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada.'}), 404
    return jsonify(tarefa.to_dict()), 200


@tasks_bp.route('/tasks', methods=['POST'])
def criar_tarefa():
    """Cria uma nova tarefa com os dados enviados no corpo da requisição."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Corpo da requisição ausente ou inválido.'}), 400

    erros = Task.validar(dados)
    if erros:
        return jsonify({'erros': erros}), 422

    tarefa = Task.criar(dados)
    return jsonify(tarefa.to_dict()), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def atualizar_tarefa(task_id):
    """Atualiza os dados de uma tarefa existente."""
    if not Task.buscar_por_id(task_id):
        return jsonify({'erro': 'Tarefa não encontrada.'}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Corpo da requisição ausente ou inválido.'}), 400

    erros = Task.validar(dados)
    if erros:
        return jsonify({'erros': erros}), 422

    tarefa = Task.atualizar(task_id, dados)
    return jsonify(tarefa.to_dict()), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def deletar_tarefa(task_id):
    """Remove permanentemente uma tarefa pelo seu ID."""
    if not Task.buscar_por_id(task_id):
        return jsonify({'erro': 'Tarefa não encontrada.'}), 404

    Task.deletar(task_id)
    return jsonify({'mensagem': 'Tarefa removida com sucesso.'}), 200
