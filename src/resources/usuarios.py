from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.usuarios import UsuariosModel

atributos = reqparse.RequestParser()
atributos.add_argument(
    "nome", type=str, required=True, help="Campo 'Nome' não pode estar em branco"
)
atributos.add_argument(
    "cpf", type=str
)
atributos.add_argument("data_nascimento", type=str)
atributos.add_argument("telefone", type=str)
atributos.add_argument(
    "email", type=str, required=True, help="Campo 'Email' não pode estar em branco"
)
atributos.add_argument(
    "senha", type=str, required=True, help="Campo 'Senha' não pode estar em branco"
)


class Usuario(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UsuariosModel.procurar_por_cpf(dados['cpf']):
            return {'mensagem': f'Usuario com cpf {dados['cpf']} ja existe'}, 403

        if UsuariosModel.procurar_por_email(dados['email']):
            return {'mensagem': f'Usuario com email {dados['email']} ja existe'}, 403

        usuario = UsuariosModel(**dados)
        try:
            usuario.salvar_usuario()
        except Exception:
            usuario.deletar_usuario()
            return {'mensagem': 'Houve algum erro interno do servidor'}, 500
        return {'mensagem': 'Cadastro concluido com sucesso!'}, 201

    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        usuario = UsuariosModel.procurar_usuario(usuario_id)
        if usuario:
            return usuario.json(), 200
        return {"mensagem": "Usuario não encontrado"}, 404

    @jwt_required()
    def put(self):
        usuario_id = get_jwt_identity()
        dados = atributos.parse_args()

        if UsuariosModel.procurar_por_email(dados['email']):
            return {'mensagem': f'O email {dados['email']} esta cadastrado!'}, 400
        if UsuariosModel.procurar_por_cpf(dados['cpf']):
            return {'mensagem': f'O cpf {dados['cpf']} esta cadastrado!'}, 400

        usuario_encontrado = UsuariosModel.procurar_usuario(usuario_id)
        if usuario_encontrado:
            try:
                usuario_encontrado.atualizar_usuario(**dados)
                usuario_encontrado.salvar_usuario()
            except Exception:
                return {'mensagem': 'Houve algum erro interno do servidor'}, 500
            return {'mensagem': 'Usuario atualizado com sucesso!'}, 200
        return {'mensagem': 'Usuario não encontrado!'}, 404

    @jwt_required()
    def delete(self, id):
        usuario_id = get_jwt_identity()
        usuario = UsuariosModel.procurar_usuario(usuario_id)

        if usuario:
            try:
                usuario.deletar_usuario()
            except Exception:
                return {'mensagem': 'Houve algum erro interno do servidor'}, 500
            return {'mensagem': 'Usuario deletado com sucesso!'}, 200
        return {'mensagem': f'Usuario com {id} não foi encontrado!'}, 404 


class LoginUsuario(Resource):
    @classmethod
    def post(cls):
        atributos_login = reqparse.RequestParser()
        atributos_login.add_argument(
            "email", type=str, required=True, help="Campo 'Email' não pode estar em branco"
        )
        atributos_login.add_argument(
            "senha", type=str, required=True, help="Campo 'Senha' não pode estar em branco"
        )
        dados = atributos_login.parse_args()
        usuario = UsuariosModel.procurar_por_email(dados['email'])
        if usuario and check_password_hash(usuario.senha, dados['senha']):
            token = create_access_token(identity=usuario.id)
            return {'token': token}, 201
        return {'mensagem': 'Email ou Senha incorreta!'}, 404
