from app import ma
from app.models import Cliente

from marshmallow import fields, validates, ValidationError

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
     
 
