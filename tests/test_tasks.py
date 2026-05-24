"""
Testes de integração para os endpoints da API de tarefas.
Cada classe cobre um grupo de rotas relacionadas.
"""


class TestListarTarefas:
    """Testes para GET /api/tasks"""

    def test_lista_vazia_sem_tarefas(self, client):
        """Sem nenhuma tarefa criada, deve retornar array vazio."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_lista_tarefas_criadas(self, client):
        """Deve listar todas as tarefas existentes no banco."""
        client.post('/api/tasks', json={'titulo': 'Tarefa A'})
        client.post('/api/tasks', json={'titulo': 'Tarefa B'})
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert len(response.get_json()) == 2


class TestCriarTarefa:
    """Testes para POST /api/tasks"""

    def test_criar_tarefa_valida(self, client):
        """Dados válidos devem retornar 201 com o objeto criado."""
        response = client.post('/api/tasks', json={
            'titulo': 'Entrega do relatório',
            'descricao': 'Enviar para o cliente até sexta',
            'prioridade': 'alta'
        })
        assert response.status_code == 201
        dados = response.get_json()
        assert dados['id'] is not None
        assert dados['titulo'] == 'Entrega do relatório'
        assert dados['status'] == 'pendente'

    def test_criar_sem_titulo_retorna_422(self, client):
        """Requisição sem título deve ser rejeitada com 422."""
        response = client.post('/api/tasks', json={'descricao': 'Sem título'})
        assert response.status_code == 422
        assert 'erros' in response.get_json()

    def test_criar_titulo_curto_retorna_422(self, client):
        """Título com menos de 3 chars deve retornar 422."""
        response = client.post('/api/tasks', json={'titulo': 'AB'})
        assert response.status_code == 422

    def test_criar_sem_corpo_retorna_400(self, client):
        """Requisição sem corpo JSON válido deve retornar 400."""
        response = client.post('/api/tasks', content_type='application/json', data='')
        assert response.status_code == 400

    def test_criar_status_invalido_retorna_422(self, client):
        """Status não reconhecido deve retornar 422."""
        response = client.post('/api/tasks', json={
            'titulo': 'Status inválido',
            'status': 'nao_existe'
        })
        assert response.status_code == 422

    def test_criar_prioridade_invalida_retorna_422(self, client):
        """Prioridade não reconhecida deve retornar 422."""
        response = client.post('/api/tasks', json={
            'titulo': 'Prioridade ruim',
            'prioridade': 'urgentissimo'
        })
        assert response.status_code == 422


class TestBuscarTarefa:
    """Testes para GET /api/tasks/<id>"""

    def test_buscar_tarefa_existente(self, client):
        """Deve retornar a tarefa correta para um ID existente."""
        criada = client.post('/api/tasks', json={'titulo': 'Buscar esta'}).get_json()
        response = client.get(f'/api/tasks/{criada["id"]}')
        assert response.status_code == 200
        assert response.get_json()['titulo'] == 'Buscar esta'

    def test_buscar_id_inexistente_retorna_404(self, client):
        """ID que não existe no banco deve retornar 404."""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404
        assert 'erro' in response.get_json()


class TestAtualizarTarefa:
    """Testes para PUT /api/tasks/<id>"""

    def test_atualizar_campos(self, client):
        """Deve persistir os novos dados e retornar o objeto atualizado."""
        criada = client.post('/api/tasks', json={'titulo': 'Antes'}).get_json()
        response = client.put(f'/api/tasks/{criada["id"]}', json={
            'titulo': 'Depois',
            'status': 'concluida',
            'prioridade': 'baixa'
        })
        assert response.status_code == 200
        dados = response.get_json()
        assert dados['titulo'] == 'Depois'
        assert dados['status'] == 'concluida'

    def test_atualizar_id_inexistente_retorna_404(self, client):
        """Atualizar tarefa inexistente deve retornar 404."""
        response = client.put('/api/tasks/9999', json={'titulo': 'Teste'})
        assert response.status_code == 404

    def test_atualizar_sem_titulo_retorna_422(self, client):
        """Atualização sem título deve retornar 422."""
        criada = client.post('/api/tasks', json={'titulo': 'Original'}).get_json()
        response = client.put(f'/api/tasks/{criada["id"]}', json={
            'descricao': 'Sem título'
        })
        assert response.status_code == 422


class TestDeletarTarefa:
    """Testes para DELETE /api/tasks/<id>"""

    def test_deletar_tarefa_existente(self, client):
        """Deve remover a tarefa e confirmar com mensagem de sucesso."""
        criada = client.post('/api/tasks', json={'titulo': 'Deletar'}).get_json()
        response = client.delete(f'/api/tasks/{criada["id"]}')
        assert response.status_code == 200
        assert 'mensagem' in response.get_json()

        # Confirmar que foi removida de fato
        busca = client.get(f'/api/tasks/{criada["id"]}')
        assert busca.status_code == 404

    def test_deletar_id_inexistente_retorna_404(self, client):
        """Deletar tarefa que não existe deve retornar 404."""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404
