from app import db
from app import models
from app.serializers import ProdutoSchema

from flask import Blueprint, abort, jsonify, request
from json import dumps as jsondump
import app.response as response
import json
from flask_restx import Api, Namespace, Resource, fields

Produto = Blueprint('Produto', __name__)
nsProduto =  Namespace("produto",  description="Operação Com Clientes")
# api =  Api(Produto)
produto_model = nsProduto.model('Produto', {
    'nome' : fields.String(required=True),
    'codigoBarras' : fields.String(required=False),
    'idFornecedor' : fields.String(required=False),
})





@nsProduto.route('/Listar', methods=['GET'])
class ClienteResource(Resource):
    def get(self):
        return listar_todos_produtos()

@nsProduto.route('/Produto/cadastrar', methods=['PUT'])
class ClienteResource(Resource):
    @nsProduto.expect(produto_model, validate=True)
    def put(self):
        return cadastrar_produto()

#Funcoes

def listar_todos_produtos():
    result = models.Produto.query.all()
    return ProdutoSchema(many=True).jsonify(result)

def cadastrar_produto():
    codigoBarras = None
    response_data = json.loads(request.data.decode())

    if 'nome' not in response_data:
        codigo, mensagem = response.bad_request("Para cadastrar um produto é preciso de um nome para ele")
        abort(codigo, mensagem)
        
    if 'idFornecedor' not in response_data:
         codigo, mensagem = response.bad_request("Para cadastrar um produto atrelar a um forneceedor")
         
    
    if  'codigoBarras' in response_data:    
        codigoBarras = response_data['codigoBarras']
    
    
    idFornecedor = response_data['idFornecedor']
    nome = response_data['nome']
    
    
    Produto_obj = models.Produto(
        nome=nome, 
        codigoBarras=codigoBarras,
        idFornecedor=idFornecedor

    )
    db.session.add(Produto_obj)
    db.session.commit()

    return {'id':Produto_obj.id}