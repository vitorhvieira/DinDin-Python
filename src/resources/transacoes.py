from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.categorias import Categorias
from models.transacoes import TransacoesModel

atributos = reqparse.RequestParser()
atributos.add_argument(
    "tipo",
    type=str,
    choices=("entrada", "saida"),
    required=True,
    help="O campo 'tipo' aceita apenas 'entrada' ou 'saida'",
)
atributos.add_argument(
    "descricao", type=str, required=True, 
    help="O campo 'descricao' é necessario"
)
atributos.add_argument(
    "valor", type=float, required=True, 
    help="O campo 'valor' é necessario!"
)
atributos.add_argument(
    "data", type=str, required=True, 
    help="O campo 'data' é necessario"
)
atributos.add_argument(
    "categoria_id", type=int, required=True, 
    help="O campo 'categoria_id' é necessario"
)


class Transacoes(Resource):
    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        transacoes = TransacoesModel.listar_transacao(usuario_id)
        if transacoes is not None:
            return [transacao.json() for transacao in transacoes], 200
        return {}, 200

    @jwt_required()
    def post(self):
        dados = atributos.parse_args()
        usuario_id = get_jwt_identity()
        dados["usuario_id"] = usuario_id
        categoria = Categorias.procurar_por_id(dados["categoria_id"])
        if categoria is None:
            return {"mensagem": f"A Categoria com id {dados["categoria_id"]} não foi encontrada!"}, 404
        transacao = TransacoesModel(**dados)
        try:
            transacao.salvar_transacao()
        except Exception:
            transacao.deletar_transacao()
            return {"mensagem": "Houve algum erro interno do servidor"}, 500
        
        return {**transacao.json(), "categoria_nome": categoria.json()["descricao"]}, 201


class Transacoes_com_id(Resource):
    @jwt_required()
    def get(self, id):
        usuario_id = get_jwt_identity()
        transacao = TransacoesModel.procurar_transacao(id)
        if transacao is not None:
            if transacao.json()["usuario_id"] == usuario_id:
                return transacao.json(), 200
            return {"mensagem": "Transação não pertence ao usuario!"}, 403
        return {"mensagem": "Transacão não encontrada"}, 404

    @jwt_required()
    def put(self, id):
        dados = atributos.parse_args()
        usuario_id = get_jwt_identity()

        if Categorias.procurar_por_id(dados["categoria_id"]) is None:
            return {"mensagem": f"A Categoria com id {dados["categoria_id"]} não foi encontrada!"}, 404

        transacao = TransacoesModel.procurar_transacao(id)

        if transacao is None:
            return {"mensagem": f"A transação {transacao} não foi encontrada!"}, 404

        if transacao is not None:
            if transacao.json()["usuario_id"] == usuario_id:
                try:
                    transacao.atualizar_transacao(**dados)
                    transacao.salvar_transacao()
                except Exception:
                    return {"mensagem": "Houve algum erro interno do servidor"}, 500
                return {"mensagem": "Transação atualizado com sucesso!"}, 200
            return {"mensagem": "Transação não pertence ao usuario logado!"}, 403
        return {"mensagem": "Transação não encontrada!"}, 404

    @jwt_required()
    def delete(self, id):
        usuario_id = get_jwt_identity()
        transacao = TransacoesModel.procurar_transacao(id)
        if transacao is not None:
            if transacao.json()["usuario_id"] == usuario_id:
                try:
                    transacao.deletar_transacao()
                except Exception:
                    return {"mensagem": "Houve algum erro interno do servidor"}, 500
                return {"mensagem": "Transação deletada com sucesso!"}, 200
            return {"mensagem": "Transação não pertence ao usuario logado!"}, 403
        return {"mensagem": "Transação não encontrada!"}, 404
