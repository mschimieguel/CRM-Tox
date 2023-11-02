from flask import Flask, render_template
from flask_restx import Api,Namespace, Resource, fields
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect,jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
ma = Marshmallow()
basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(version='1.0', title='Message Monitor', description='API documentation of Message Monitor',doc="/swagger")


api.init_app(app)
 
@api.route('/index', methods=['GET'])
class IndexResource(Resource):
    def get(self):
        return render_template("index.html")
    
class Grupos(db.Model):
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    fonte = db.Column(db.String(100), nullable=False)
    dataExclusao = db.Column(db.DateTime, nullable=True)
    def __init__(
                self,
                nome,
                fonte,
                dataExclusao=None
            ):
        self.id = id
        self.nome = nome
        self.fonte = fonte
        self.dataExclusao = dataExclusao
               
    def __repr__(self):
        return f'<Grupo {self.firstname}>'

class GrupoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grupos
        load_instance = True

    nome = fields.String(required=True, description="Nome Grupo")
    fonte = fields.String(required=False, description="fonte de dados")
    dataExlusao = fields.String(required=False, description="data de exclusao")

nsGrupo = Namespace("Grupo",  description="Operação Com Grupos")
api.add_namespace(nsGrupo)

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
        codigo, mensagem = bad_request("Cliente Nao Encontrado")
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

def success(data:dict = None):
    response = {
        'success': True,
        'message': 'Operation successful',
        'data': data
     }
    return jsonify(response), 200


def bad_request(mensagem: str):
    response = {
        'success': False,
        'message': "Bad request: " + mensagem
    }
    return 400,response