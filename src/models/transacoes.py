from db.database import database


class TransacoesModel(database.Model):
    __tablename__ = "transacoes"

    id = database.Column(database.Integer, primary_key=True)
    tipo = database.Column(database.String(40), nullable=False)
    descricao = database.Column(database.String(40), nullable=False)
    valor = database.Column(database.Integer, nullable=False)
    data = database.Column(database.String(50), nullable=False)
    categoria_id = database.Column(
        database.Integer, database.ForeignKey("categorias.id"), nullable=False
    )
    usuario_id = database.Column(
        database.Integer, database.ForeignKey("usuarios.id"), nullable=False
    )

    def __init__(self, tipo, descricao, valor, data, categoria_id, usuario_id):
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id

    def json(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "data": self.data,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
        }

    def atualizar_transacao(self, tipo, descricao, valor, data, categoria_id):
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria_id = categoria_id

    @classmethod
    def procurar_transacao(cls, id):
        transacao = cls.query.filter_by(id=id).first()
        if transacao:
            return transacao
        return None

    @classmethod
    def listar_transacao(cls, usuario_id):
        transacao = cls.query.filter_by(usuario_id=usuario_id).all()
        if transacao:
            return transacao
        return None

    def salvar_transacao(self):
        database.session.add(self)
        database.session.commit()

    def deletar_transacao(self):
        database.session.delete(self)
        database.session.commit()
