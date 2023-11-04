from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_restx import Api,Namespace, Resource, fields
import os
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect,jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, validates, ValidationError
import app.response as response
import app.pipelineValidacoes as pipelineValidacoes
import app.bodyParameter  as bodyParameter
import app.alterarAtributoBd as alterarAtributoBd
from datetime import datetime
import re
from datetime import datetime
import json
import packages.validadores as validadores

def converter_AAAA_MM_DD(data):
    if data is None:
        return None
    return datetime.strptime(data, "%Y-%m-%d")
from sqlalchemy.sql import func
ma = Marshmallow()
basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(version='1.0', title='CRM', description='API documentation of A Simple',doc="/swagger")


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


nsCliente = Namespace("Clientes",  description="Operação Com Clientes")
api.add_namespace(nsCliente)

class Cliente(db.Model):

    __tablename__ = 'clientes'  # Real table name, since is case sensitive

    id = db.Column(db.Integer, primary_key=True)
    CPF_CNPJ = db.Column(db.String,nullable=True,unique=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    telefone = db.Column(db.String, nullable=True)
    whatsapp = db.Column(db.String, nullable=True)
    celular = db.Column(db.String, nullable=True)
    dataExclusao = db.Column(db.DateTime, nullable=True)
    dataNascimento = db.Column(db.DateTime, nullable=True)

    def __init__(
                self,
                nome,
                CPF_CNPJ=None,
                email=None,
                telefone=None,
                whatsapp=None,
                celular=None,
                dataExclusao=None,
                dataNascimento=None
            ):
        """Constructor to help write data"""

        self.nome = nome
        self.CPF_CNPJ = CPF_CNPJ
        self.email = email
        self.telefone = telefone
        self.whatsapp = whatsapp
        self.celular = celular
        self.dataExclusao = dataExclusao
        self.dataNascimento = dataNascimento

    def __repr__(self) -> str:
        """Object representation"""
        return self.nome

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True

    CPF_CNPJ = fields.String(required=False, description="identificador de Cliente PF ou PJ")
    nome = fields.String(required=True, description="Nome cliente")
    email = fields.String(required=False, description="endereco de email")
    telefone = fields.String(required=False,description="telefone")
    whatsapp = fields.String(required=False,description="User's name")
    celular = fields.String(required=False,description="User's name")
    dataExlusao = fields.String(required=False, description="User's name")
    dataNascimento = fields.String(required=False,description="User's name")

    @validates('id')
    def validate_id(self, value):
        raise ValidationError('Never send the id')
     
# cliente_model = nsCliente.model('Cliente', {
#     'CPF_CNPJ': fields.String(required=False, description="identificador de Cliente PF ou PJ"),
#     'nome': fields.String(required=False, description="Nome cliente"),
#     'email': fields.String(required=False, description="endereco de email"),
#     'telefone': fields.String(required=False,description="telefone"),
#     'whatsapp': fields.String(required=False,description="whatsapp para contato"),
#     'celular': fields.String(required=False,description="User's name"),
#     'dataNascimento': fields.String(required=False,description="User's name")
# })


# # ROTAS 
# @nsCliente.route('/cadastrar', methods=['PUT'])
# class ClienteResource(Resource):
#     @nsCliente.expect(cliente_model, validate=True)
#     def put(self):
#         return cadastrarCliente()
    
@nsCliente.route("/listarTodos",methods=['GET'])
class ClienteResource(Resource):
    def get(self):
        return listarTodosClientes()
    
@nsCliente.route('/listarPessoaJuridica',methods=['GET'])
class ClientePJResource(Resource):
    def get(self):
        return listarPessoaJuridica()

@nsCliente.route('/listarPessoaFisica', methods=['GET'])
class ClientePFResnomeAtributoource(Resource):
    def get(self):
        return listarPessoaFisica()
    
# @nsCliente.route('/<id>/atualizar', methods=['PATCH'])
# class ClienteResource(Resource):
#     @nsCliente.expect(cliente_model, validate=True)
#     def patch(self,id):
#         return atualizarCadastroCliente(id)
    
# @nsCliente.route('/<id>/apagarAtributo/<nomeAtributo>', methods=['DELETE'])
# class ClienteResource(Resource):
#     def delete(self,id):
#         return apagarAtributo(id)
    
  
@nsCliente.route('/<id>/deletar', methods=['DELETE'])
class ClienteResource(Resource):
    def delete(self,id):
        return deletarCliente(id)
    

#Funcoes

def cadastrarCliente():
    response_data = json.loads(request.data.decode())
    CPF_CNPJ = bodyParameter.get(response_data,'cpf_cnpj')
    nome = bodyParameter.get(response_data,'nome')
    email = bodyParameter.get(response_data,'email')
    telefone = bodyParameter.get(response_data,'telefone')
    whatsapp = bodyParameter.get(response_data,'whatsapp')
    celular = bodyParameter.get(response_data,'celular')
    dataNascimento = bodyParameter.get(response_data,'dataNascimento')
    
    resultado,mensagem = pipelineValidacoes.Executar(
        [
            ('nome' in response_data,"Para cadastrar um cliente é preciso de um nome"),
            (validadores.validarCPF_CNPJ(CPF_CNPJ), "CPF ou CNPJ invalido."),
            (validadores.validarEmail(email), "Email Invalido"),
            (validadores.validarTelefoneFixo(telefone), "Telefone Fixo Invalido"),
            (validadores.validarData(dataNascimento), "Data de nascimento Invalida"),
            (validadores.validarCelular(celular), "Celular Invalido"),
            ( Cliente.query.filter_by(CPF_CNPJ=CPF_CNPJ).first() is None,"Ja existe um usario com esse CPF/CNPJ" )
        ]
    )
    
    if resultado is False: 
        codigo, mensagem = response.bad_request(mensagem)
        abort(codigo, mensagem)

    cliente_obj = Cliente(
        CPF_CNPJ = CPF_CNPJ,
        nome = nome,
        email = email,
        telefone = telefone,
        whatsapp = whatsapp,
        celular = celular,
        dataNascimento =  datetime.strptime(dataNascimento, "%Y-%m-%d")
    )

    db.session.add(cliente_obj)

    db.session.commit()
    
    return {'id':cliente_obj.id}

def listarPessoaFisica():
    result = Cliente.query.filter(Cliente.CPF_CNPJ.ilike('___.___.___-__')).filter_by(dataExclusao=None).all()
    return ClienteSchema(many=True).jsonify(result)

def listarPessoaJuridica():
    result = Cliente.query.filter(Cliente.CPF_CNPJ.ilike('__.___.___/____-__')).filter_by(dataExclusao=None).all()
    return ClienteSchema(many=True).jsonify(result)

def listarTodosClientes():
    result = Cliente.query.filter_by(dataExclusao=None).all()
    return ClienteSchema(many=True).jsonify(result)

def atualizarCadastroCliente(id):
    response_data = json.loads(request.data.decode())
    
    CPF_CNPJ = bodyParameter.get(response_data,'CPF_CNPJ')
    print("CPF_CNPJ",CPF_CNPJ)
    nome = bodyParameter.get(response_data,'nome')
    email = bodyParameter.get(response_data,'email')
    telefone = bodyParameter.get(response_data,'telefone')
    whatsapp = bodyParameter.get(response_data,'whatsapp')
    celular = bodyParameter.get(response_data,'celular')
    dataNascimento = bodyParameter.get(response_data,'dataNascimento')
    
    
    resultado,mensagem = pipelineValidacoes.Executar(
        [
            
            (validadores.validarCPF_CNPJ(CPF_CNPJ), "CPF ou CNPJ invalido."),
            (validadores.validarEmail(email), "Email Invalido"),
            (validadores.validarTelefoneFixo(telefone), "Telefone Fixo Invalido"),
            (validadores.validarData(dataNascimento), "Data de nascimento Invalida"),
            (validadores.validarCelular(celular), "Celular Invalido"),
        ]
    )
    if resultado is False: 
        codigo, mensagem =  response.bad_request(mensagem)
        abort(codigo, mensagem)
        
    cliente_obj = Cliente.query.filter_by(id=id).filter_by(dataExclusao=None).first()
    if cliente_obj is None:
        codigo, mensagem =  response.bad_request("Cliente Nao Encontrado")
        abort(codigo, mensagem)


    alterarAtributoBd._(cliente_obj, 'nome', nome)
    alterarAtributoBd._(cliente_obj, 'email', email)
    alterarAtributoBd._(cliente_obj, 'whatsapp', whatsapp)
    alterarAtributoBd._(cliente_obj, 'dataNascimento',  converter_AAAA_MM_DD(dataNascimento))
    print("CPF_CNPJ",CPF_CNPJ)
    alterarAtributoBd._(cliente_obj, 'CPF_CNPJ', CPF_CNPJ)

    db.session.commit()
    
    return True