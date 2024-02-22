from db.database import database


class Categorias(database.Model):
    __tablename__ = "categorias"

    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String, nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao

    def json(self):
        return {"id": self.id, "descricao": self.descricao}

    @classmethod
    def procurar_por_id(cls, id):
        categoria = cls.query.filter_by(id=id).first()
        if categoria:
            return categoria
        return None
