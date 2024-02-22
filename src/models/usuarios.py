from db.database import database
from flask_bcrypt import generate_password_hash


class UsuariosModel(database.Model):
    __tablename__ = "usuarios"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(40), nullable=False, unique=True)
    cpf = database.Column(database.String(14), nullable=False, unique=True)
    data_nascimento = database.Column(database.String(10))
    telefone = database.Column(database.String(20))
    senha = database.Column(database.String, nullable=False)

    def __init__(self, nome, email, cpf, data_nascimento, telefone, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.senha = generate_password_hash(senha, 10).decode("utf8")

    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "email": self.email,
        }

    @classmethod
    def procurar_usuario(cls, id):
        usuario = cls.query.filter_by(id=id).first()

        if usuario:
            return usuario
        return None

    @classmethod
    def procurar_por_email(cls, email):
        email = cls.query.filter_by(email=email).first()

        if email:
            return email
        return None

    @classmethod
    def procurar_por_cpf(cls, cpf):
        cpf = cls.query.filter_by(cpf=cpf).first()
        if cpf:
            return cpf
        return None

    def atualizar_usuario(self, nome, email, cpf, data_nascimento, telefone, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.senha = generate_password_hash(senha, 10).decode("utf8")

    def salvar_usuario(self):
        database.session.add(self)
        database.session.commit()

    def deletar_usuario(self):
        database.session.delete(self)
        database.session.commit()
