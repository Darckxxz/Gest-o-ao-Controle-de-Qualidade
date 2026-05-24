import os
import tempfile
import pytest
from src import database
from src.app import create_app


@pytest.fixture
def app():
    """
    Cria uma instância isolada da aplicação para cada teste.
    Usa banco de dados temporário para não afetar dados reais.
    """
    # Arquivo temporário descartado ao fim de cada teste
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    database.set_database_path(db_path)

    application = create_app(testing=True)

    yield application

    # Limpeza: fecha e remove o banco temporário
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Retorna o cliente HTTP de testes do Flask."""
    return app.test_client()
