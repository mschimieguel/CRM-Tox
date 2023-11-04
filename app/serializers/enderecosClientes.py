from app import ma
from app.models import EnderecosCliente

from marshmallow import fields, validates, ValidationError

class EnderecosClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EnderecosCliente
        load_instance = True
   
    idCliente = fields.Str(required=True)
    CEP = fields.Str(required=True)
    estado = fields.Str(required=True)
    cidade = fields.Str(required=True)
    logradouro = fields.Str(required=True)
    numero = fields.Str(required=True)

    @validates('id')
    def validate_id(self, value):
        raise ValidationError('Never send the id')