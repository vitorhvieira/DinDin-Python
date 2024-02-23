import os

import dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.categorias import Categoria
from resources.extrato import Extrato
from resources.transacoes import Transacoes, Transacoes_com_id
from resources.usuarios import LoginUsuario, Usuario

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_DATA")}"
)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Usuario, "/usuario/")
api.add_resource(LoginUsuario, "/login")
api.add_resource(Categoria, "/categoria")
api.add_resource(Transacoes, "/transacao")
api.add_resource(Transacoes_com_id, "/transacao/<int:id>")
api.add_resource(Extrato, "/transacao/extrato")


if __name__ == "__main__":
    from db.database import database

    database.init_app(app)
    app.run(debug=True)
