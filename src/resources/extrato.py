from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.transacoes import TransacoesModel


class Extrato(Resource):
    @jwt_required()
    def get(self):
        usuario = get_jwt_identity()
        transacoes = TransacoesModel.listar_transacao(usuario)

        if transacoes:
            entrada = sum(
                transacao.valor
                for transacao in transacoes
                if transacao.tipo == "entrada"
            )
            saida = sum(
                transacao.valor for transacao in transacoes if transacao.tipo == "saida"
            )
            return {"entrada": entrada, "saida": saida}, 200
        return {"mensagem": "Nenhuma transação encontrada."}, 404
