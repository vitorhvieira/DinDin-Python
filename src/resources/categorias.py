from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.categorias import Categorias


class Categoria(Resource):
    @jwt_required()
    def get(self):
        return {
            "Categorias": [categoria.json() for categoria in Categorias.query.all()]
        }, 200
