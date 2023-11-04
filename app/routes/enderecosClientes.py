from app import db
from app import models
from app.serializers import EnderecosClienteSchema


from datetime import datetime
from flask import Blueprint, jsonify, request
from json import dumps as jsondump
import json
import app.response as response
from flask_restx import Api, Namespace, Resource, fields

enderecoscliente = Blueprint('enderecoscliente', __name__)
# api =  Api(enderecoscliente)
nsEnderecoCliente = Namespace(name="Endereco De Clientes", path="/cliente/enderecos",  description="Operação Com Endereco De Clientes")

endereco_cliente_model = nsEnderecoCliente.model('EnderecoCliente', {
    'idCliente' : fields.String(required=True),
    'CEP' : fields.String(required=True),
    'estado' : fields.String(required=True),
    'cidade' : fields.String(required=True),
    'logradouro' : fields.String(required=True),
    'numero' : fields.String(required=True)
})

#rotas

@nsEnderecoCliente.route('/<idCliente>/listar',methods=['GET'])
class EnderecoClienteResource(Resource):
    def get(self,idCliente):
        return listarEnderecosCliente(idCliente)

@nsEnderecoCliente.route('/<idCliente>/cadastrar', methods=['PUT'])
class EnderecoClienteResource(Resource):
    @nsEnderecoCliente.expect(endereco_cliente_model, validate=True)
    def put(self,idCliente):
        return cadastrarEnderecoCliente(idCliente)

# api.add_namespace(nsEnderecoCliente)
#Funcoes 


def listarEnderecosCliente(idCliente):
    result = models.EnderecosCliente.query.filter_by(idCliente=idCliente).all()
    return EnderecosClienteSchema(many=True).jsonify(result)


def cadastrarEnderecoCliente(idCliente):
    response_data = json.loads(request.data.decode())

    cep = response_data['CEP']
    estado = response_data['estado']
    cidade = response_data['cidade']
    logradouro = response_data['logradouro']
    numero = response_data['numero']

    enderecoCliente_obj = models.EnderecosCliente(
        idCliente = idCliente,
        CEP = cep,
        estado = estado,
        cidade = cidade,
        logradouro = logradouro,
        numero = numero
    )

    db.session.add(enderecoCliente_obj)
    db.session.commit()
   
    return  response.success()