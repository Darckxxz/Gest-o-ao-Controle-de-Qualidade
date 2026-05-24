import os
import tempfile
import pytest
from src import database
from src.database import init_database
from src.models.task import Task


@pytest.fixture(autouse=True)
def banco_temporario():
    """Cria e destrói um banco de dados temporário para cada teste unitário."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    database.set_database_path(db_path)
    init_database()
    yield
    os.close(db_fd)
    os.unlink(db_path)


# ---------------------------------------------------------------------------
# Testes de validação
# ---------------------------------------------------------------------------

class TestValidacao:
    """Verifica as regras de validação do modelo Task."""

    def test_titulo_vazio_retorna_erro(self):
        """Título vazio deve gerar mensagem de erro."""
        erros = Task.validar({'titulo': ''})
        assert len(erros) > 0
        assert any('titulo' in e for e in erros)

    def test_titulo_muito_curto_retorna_erro(self):
        """Título com menos de 3 caracteres deve ser rejeitado."""
        erros = Task.validar({'titulo': 'AB'})
        assert len(erros) > 0

    def test_titulo_valido_sem_erros(self):
        """Título com 3 ou mais caracteres não deve gerar erros."""
        erros = Task.validar({'titulo': 'Tarefa válida'})
        assert erros == []

    def test_status_invalido_retorna_erro(self):
        """Status fora dos valores aceitos deve gerar erro."""
        erros = Task.validar({'titulo': 'Teste', 'status': 'errado'})
        assert any('status' in e.lower() for e in erros)

    def test_todos_status_validos_sem_erro(self):
        """Cada status válido individualmente não deve gerar erros."""
        for status in Task.STATUS_VALIDOS:
            assert Task.validar({'titulo': 'Teste', 'status': status}) == []

    def test_prioridade_invalida_retorna_erro(self):
        """Prioridade não reconhecida deve gerar mensagem de erro."""
        erros = Task.validar({'titulo': 'Teste', 'prioridade': 'urgente'})
        assert any('prioridade' in e.lower() for e in erros)

    def test_todas_prioridades_validas_sem_erro(self):
        """Cada prioridade válida individualmente não deve gerar erros."""
        for prioridade in Task.PRIORIDADES_VALIDAS:
            assert Task.validar({'titulo': 'Teste', 'prioridade': prioridade}) == []


# ---------------------------------------------------------------------------
# Testes de operações CRUD
# ---------------------------------------------------------------------------

class TestCRUD:
    """Testa as operações de banco de dados do modelo Task."""

    def test_criar_retorna_tarefa_com_id(self):
        """Criar uma tarefa deve retornar objeto com ID gerado."""
        tarefa = Task.criar({'titulo': 'Nova Tarefa'})
        assert tarefa is not None
        assert tarefa.id is not None
        assert tarefa.titulo == 'Nova Tarefa'

    def test_criar_com_valores_padrao(self):
        """Campos opcionais devem ter valores padrão definidos."""
        tarefa = Task.criar({'titulo': 'Padrão'})
        assert tarefa.status == 'pendente'
        assert tarefa.prioridade == 'media'

    def test_buscar_todos_lista_vazia(self):
        """Sem tarefas no banco, deve retornar lista vazia."""
        assert Task.buscar_todos() == []

    def test_buscar_todos_retorna_criadas(self):
        """Deve listar exatamente as tarefas inseridas."""
        Task.criar({'titulo': 'T1'})
        Task.criar({'titulo': 'T2'})
        assert len(Task.buscar_todos()) == 2

    def test_buscar_por_id_encontra_tarefa(self):
        """Deve retornar a tarefa correta ao buscar pelo ID."""
        criada = Task.criar({'titulo': 'Buscar'})
        encontrada = Task.buscar_por_id(criada.id)
        assert encontrada is not None
        assert encontrada.titulo == 'Buscar'

    def test_buscar_por_id_inexistente_retorna_none(self):
        """ID inexistente deve retornar None."""
        assert Task.buscar_por_id(9999) is None

    def test_atualizar_altera_campos(self):
        """Atualização deve refletir os novos valores no banco."""
        tarefa = Task.criar({'titulo': 'Antes'})
        atualizada = Task.atualizar(
            tarefa.id,
            {'titulo': 'Depois', 'status': 'concluida', 'prioridade': 'alta'}
        )
        assert atualizada.titulo == 'Depois'
        assert atualizada.status == 'concluida'
        assert atualizada.prioridade == 'alta'

    def test_deletar_remove_tarefa(self):
        """Após deletar, tarefa não deve ser encontrada no banco."""
        tarefa = Task.criar({'titulo': 'Remover'})
        resultado = Task.deletar(tarefa.id)
        assert resultado is True
        assert Task.buscar_por_id(tarefa.id) is None

    def test_to_dict_contem_campos_esperados(self):
        """Serialização para dict deve incluir todos os campos da API."""
        tarefa = Task.criar({'titulo': 'Serializar', 'descricao': 'Desc'})
        d = tarefa.to_dict()
        for campo in ['id', 'titulo', 'descricao', 'status', 'prioridade']:
            assert campo in d
