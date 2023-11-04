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


nsCliente = Namespace("cliente",  description="Operação Com Clientes")
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
     
cliente_model = nsCliente.model('Cliente', {
    'CPF_CNPJ': fields.String(required=False, description="identificador de Cliente PF ou PJ"),
    'nome': fields.String(required=False, description="Nome cliente"),
    'email': fields.String(required=False, description="endereco de email"),
    'telefone': fields.String(required=False,description="telefone"),
    'whatsapp': fields.String(required=False,description="whatsapp para contato"),
    'celular': fields.String(required=False,description="User's name"),
    'dataNascimento': fields.String(required=False,description="User's name"),
})


# ROTAS 
@nsCliente.route('/cadastrar', methods=['PUT'])
class ClienteResource(Resource):
    @nsCliente.expect(cliente_model, validate=True)
    def put(self):
        return cadastrarCliente()
    
@nsCliente.route("/listarTodos",methods=['GET'])
class ClienteResource(Resource):
    def get(self):
        return listarTodosClientes()
    
@nsCliente.route('/listarPessoaJuridica',methods=['GET'])
class ClientePJResource(Resource):
    def get(self):
        return listarPessoaJuridica()

@nsCliente.route('/listarPessoaFisica', methods=['GET'])
class ClientePFResource(Resource):
    def get(self):
        return listarPessoaFisica()
    
@nsCliente.route('/<id>/atualizar', methods=['PATCH'])
class ClienteResource(Resource):
    @nsCliente.expect(cliente_model, validate=True)
    def patch(self,id):
        return atualizarCadastroCliente(id)
    
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
            (validarCPF_CNPJ(CPF_CNPJ), "CPF ou CNPJ invalido."),
            (validarEmail(email), "Email Invalido"),
            (validarTelefoneFixo(telefone), "Telefone Fixo Invalido"),
            (validarData(dataNascimento), "Data de nascimento Invalida"),
            (validarCelular(celular), "Celular Invalido"),
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
            
            (validarCPF_CNPJ(CPF_CNPJ), "CPF ou CNPJ invalido."),
            (validarEmail(email), "Email Invalido"),
            (validarTelefoneFixo(telefone), "Telefone Fixo Invalido"),
            (validarData(dataNascimento), "Data de nascimento Invalida"),
            (validarCelular(celular), "Celular Invalido"),
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


def deletarCliente(id):
    cliente_obj = Cliente.query.filter_by(id=id).first()
    if cliente_obj is None:
        codigo, mensagem = response.bad_request("Cliente Nao Encontrado")
        abort(codigo, mensagem)
    dataExclusao =  datetime.now()
    setattr(cliente_obj, 'dataExclusao', dataExclusao)
    db.session.commit()
    return True
    
def validarCPF(cpf:str) -> bool:
    if cpf is None:
      return True
    if cpf=='': 
      return False
    
    cpf_standard = re.compile("[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}$")
    legal_format = cpf_standard.match(cpf)
    if(not legal_format):
      return False
    
    cpf = cpf.replace('.', '')
    cpf = cpf.replace('-', '')
    init_cpf = cpf
    cpf = cpf[:9]
    
    checksum = 0
    mult = 10
    for num in range(9):
        checksum += int(cpf[num]) * (mult - int(num))
    rest = checksum % 11
    if(rest<2):
        first_digit = 0
    else:
        first_digit = 11-rest
    cpf += str(first_digit)

    checksum = 0
    mult = 11
    for num in range(10):
        checksum += int(cpf[num]) * (mult - int(num))
    rest = checksum % 11
    if(rest<2):
        second_digit = 0
    else:
        second_digit = 11-rest
    cpf += str(second_digit)

    return cpf==init_cpf

def validarCNPJ(cnpj:str) -> bool:
  if(cnpj is None):
    return True
  if cnpj == '': 
      return False
  
  cnpj_standard = re.compile("[0-9]{2}[.][0-9]{3}[.][0-9]{3}[/][0-9]{4}[-][0-9]{2}$")
  legal_format = cnpj_standard.match(cnpj)
  if(not legal_format):
    return False
  
  cnpj = cnpj.replace('.', '')
  cnpj = cnpj.replace('-', '')
  cnpj = cnpj.replace('/', '')
  init_cnpj = cnpj
  cnpj = cnpj[:12]

  checksum = 0
  mult = [5,4,3,2,9,8,7,6,5,4,3,2]
  for num in range(12):
    checksum += int(cnpj[num]) * mult[num]
  rest = checksum % 11
  if(rest<2):
    first_digit = 0
  else:
    first_digit = 11 - rest
  cnpj += str(first_digit)

  checksum = 0
  mult = [6,5,4,3,2,9,8,7,6,5,4,3,2]
  for num in range(13):
    checksum += int(cnpj[num]) * mult[num]
  rest = checksum % 11
  if(rest<2):
    second_digit = 0
  else:
    second_digit = 11 - rest
  cnpj += str(second_digit)

  return cnpj==init_cnpj

def validarCPF_CNPJ(cpfCnpj:str) -> bool:
  return validarCPF(cpfCnpj) or validarCNPJ(cpfCnpj)

def validarEmail(email:str) -> bool:
  if(email==None):
    return True
  if email == '': 
      return False
  size = len(email)
  at, dot, dot_before_at ,dot_after_at = 0, 0, 0, 0
  for i in range(size):
    symbol = email[i]
    if(symbol=='@'):
      if(at>0):
        return False
      at += 1
      if(i<3):
        return False
    elif(at>0):
      if(dot>0):
        dot_after_at += 1
      elif(symbol=='.'):
        dot = 1
        if(dot_before_at<3):
          return False
      else:
        dot_before_at += 1
  if(i+1==size and dot_after_at>1):
    return True
  else:
    return False

def validarCelular(celular:str) -> bool:
  if(celular==None):
    return True
  if celular == '': 
      return False
  padrao = r'\(\d{2}\) (9\d{4}-\d{4}|\d{4}-\d{4})'  # padrão regex para '(XX) 9XXXX-XXXX' ou '(XX) XXXX-XXXX'

  if re.match(padrao, celular):
      return True
  else:
      return False

# Validadores

def validarTelefoneFixo(telefoneFixo: str) -> bool:
  if(telefoneFixo==None):
    return True
  if telefoneFixo == '': 
      return False
  telefoneFixo = telefoneFixo.replace('+', '')
  telefoneFixo = telefoneFixo.replace('(', '')
  telefoneFixo = telefoneFixo.replace(')', '')
  telefoneFixo = telefoneFixo.replace('-', '')
  telefoneFixo = telefoneFixo.replace(' ', '')
  telefoneFixo = telefoneFixo.removeprefix('0')

  size = len(telefoneFixo)
  
  ddds = re.compile("(1[1-9]|2[12478]|3[1-578])|4[1-9]|5[13-5]|6[1-9]|7[13-579]|8[1-9]|9[1-9]")
  valid_ddd = ddds.match(telefoneFixo)
  if(not valid_ddd):
    return False
  
  if(size!=10):
    return False

  valid_prefixes = ['2','3','4','5']
  if(telefoneFixo[-8] not in valid_prefixes):
    return False
  
  return True

def validarCEP(cep: str) -> bool:
  if(cep==None):
    return True
  
  cep_standard = re.compile("[0-9]{2}[.][0-9]{3}[-][0-9]{3}$")
  legal_format = cep_standard.match(cep)
  if(not legal_format):
    return False
  return True

def validarCodigoBarras(codigoBarras: str) -> bool:
  return True 

def validarData(data: str) -> bool:
  if data == None: 
      return True
  if data == '': 
      return False
  formato = "%Y-%m-%d"
  try:
      datetime.strptime(data, formato)
      return True
  except ValueError:
      return False
  
def validarEstado(estado: str) -> bool:
  if estado is None:
    return False
  estados = {'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'}
  return estado.upper() in estados

def validarNumero(numero: str) -> bool:
  if numero is None:
    return False
  return numero.isnumeric()