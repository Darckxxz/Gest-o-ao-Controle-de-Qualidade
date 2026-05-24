from src.database import get_connection


class Task:
    """Representa uma tarefa no sistema TaskFlow."""

    # Valores válidos para o campo status
    STATUS_VALIDOS = ['pendente', 'em_progresso', 'concluida']

    # Valores válidos para o campo prioridade
    PRIORIDADES_VALIDAS = ['baixa', 'media', 'alta']

    def __init__(self, id=None, titulo=None, descricao='',
                 status='pendente', prioridade='media',
                 criado_em=None, atualizado_em=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prioridade = prioridade
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self):
        """Serializa a instância para dicionário (compatível com JSON)."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'prioridade': self.prioridade,
            'criado_em': str(self.criado_em) if self.criado_em else None,
            'atualizado_em': str(self.atualizado_em) if self.atualizado_em else None,
        }

    @staticmethod
    def validar(dados):
        """Valida os dados de entrada. Retorna lista de mensagens de erro."""
        erros = []

        titulo = dados.get('titulo', '').strip()
        if not titulo:
            erros.append('O campo "titulo" é obrigatório.')
        elif len(titulo) < 3:
            erros.append('O campo "titulo" deve ter no mínimo 3 caracteres.')

        if 'status' in dados and dados['status'] not in Task.STATUS_VALIDOS:
            erros.append(
                f'Status inválido. Valores aceitos: {Task.STATUS_VALIDOS}'
            )

        if 'prioridade' in dados and dados['prioridade'] not in Task.PRIORIDADES_VALIDAS:
            erros.append(
                f'Prioridade inválida. Valores aceitos: {Task.PRIORIDADES_VALIDAS}'
            )

        return erros

    @staticmethod
    def buscar_todos():
        """Retorna todas as tarefas ordenadas da mais recente para a mais antiga."""
        conn = get_connection()
        rows = conn.execute(
            'SELECT * FROM tasks ORDER BY criado_em DESC'
        ).fetchall()
        conn.close()
        return [Task(**dict(row)) for row in rows]

    @staticmethod
    def buscar_por_id(task_id):
        """Busca uma tarefa pelo ID. Retorna None se não encontrada."""
        conn = get_connection()
        row = conn.execute(
            'SELECT * FROM tasks WHERE id = ?', (task_id,)
        ).fetchone()
        conn.close()
        return Task(**dict(row)) if row else None

    @staticmethod
    def criar(dados):
        """Insere uma nova tarefa no banco e retorna o objeto criado."""
        conn = get_connection()
        cursor = conn.execute(
            '''
            INSERT INTO tasks (titulo, descricao, status, prioridade)
            VALUES (?, ?, ?, ?)
            ''',
            (
                dados['titulo'].strip(),
                dados.get('descricao', ''),
                dados.get('status', 'pendente'),
                dados.get('prioridade', 'media'),
            )
        )
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Task.buscar_por_id(task_id)

    @staticmethod
    def atualizar(task_id, dados):
        """Atualiza os campos de uma tarefa existente e retorna o objeto atualizado."""
        conn = get_connection()
        conn.execute(
            '''
            UPDATE tasks
            SET titulo = ?, descricao = ?, status = ?, prioridade = ?,
                atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (
                dados['titulo'].strip(),
                dados.get('descricao', ''),
                dados.get('status', 'pendente'),
                dados.get('prioridade', 'media'),
                task_id,
            )
        )
        conn.commit()
        conn.close()
        return Task.buscar_por_id(task_id)

    @staticmethod
    def deletar(task_id):
        """Remove a tarefa do banco. Retorna True se alguma linha foi afetada."""
        conn = get_connection()
        cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
