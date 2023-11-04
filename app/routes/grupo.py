from flask import abort
from app.models.grupo import Grupos
from app.models.rdb import db
from datetime import datetime
from app.serializers.grupo import GrupoSchema
import app.response as response
from flask_restx import Namespace, Resource
from datetime import datetime

nsGrupo = Namespace("Grupo",  description="Operação Com Grupos")

@nsGrupo.route('/grupo', methods=['GET','PUT'])
class GrupoResource(Resource):
    def get(self):
        return listarTodosGrupos()
    @nsGrupo.expect(GrupoSchema, validate=True)
    def put(self):
         return cadastrarGrupo(id)
    
@nsGrupo.route('/grupo/<id>', methods=['PATCH','DELETE'])
class GrupoResource(Resource):
    def patch(self,id):
        return alterarGrupo(id)
    def delete(self,id):
        return deletarGrupo(id)
    
def deletarGrupo(id):
    cliente_obj = Grupos.query.filter_by(id=id).first()
    if cliente_obj is None:
        codigo, mensagem = response.bad_request("Cliente Nao Encontrado")
        abort(codigo, mensagem)
    dataExclusao =  datetime.now()
    setattr(cliente_obj, 'dataExclusao', dataExclusao)
    db.session.commit()
    return True

def cadastrarGrupo(id):
    return True

def alterarGrupo(id):
    return True

def listarTodosGrupos():
    result = Grupos.query.all()
    return GrupoSchema(many=True).jsonify(result)