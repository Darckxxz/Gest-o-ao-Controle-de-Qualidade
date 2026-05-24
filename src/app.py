from flask import Flask, jsonify
from src.database import init_database, set_database_path
from src.routes.tasks import tasks_bp
from src.routes.auth import auth_bp


def create_app(testing=False, db_path=None):
    """
    Fábrica de aplicação Flask (Application Factory pattern).
    Permite criar instâncias isoladas para testes.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'taskflow-dev-secret-2024'

    if testing:
        app.config['TESTING'] = True

    # Permite que os testes injetem um banco de dados temporário
    if db_path:
        set_database_path(db_path)

    # Registra os módulos de rotas com prefixo /api
    app.register_blueprint(tasks_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Rota raiz com informações e mapa de endpoints da API."""
        return jsonify({
            'projeto': 'TaskFlow',
            'descricao': 'Sistema de Gerenciamento de Tarefas - TechFlow Solutions',
            'versao': '1.0.0',
            'cliente': 'LogiTrack Startup de Logística',
            'endpoints': {
                'GET  /api/tasks': 'Listar todas as tarefas',
                'POST /api/tasks': 'Criar nova tarefa',
                'GET  /api/tasks/<id>': 'Buscar tarefa por ID',
                'PUT  /api/tasks/<id>': 'Atualizar tarefa',
                'DELETE /api/tasks/<id>': 'Remover tarefa',
                'POST /api/auth/registro': 'Registrar usuário',
                'POST /api/auth/login': 'Autenticar usuário',
            }
        })

    # Inicializa o esquema do banco de dados na criação da aplicação
    init_database()

    return app
