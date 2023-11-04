from app import ma
from app.models import Produto

from marshmallow import fields, validates, ValidationError

class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True

    nome = fields.Str(required=True)
    codigoBarras = fields.Str(required=False)
    idFornecedor =fields.Str(required=False)

    @validates('id')
    def validate_id(self, value):
        raise ValidationError('Never send the id')