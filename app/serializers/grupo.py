from app import ma
from app.models import Grupos

from marshmallow import fields

class GrupoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grupos
        load_instance = True

    nome = fields.String(required=True, description="Nome Grupo")
    fonte = fields.String(required=False, description="fonte de dados")
    dataExlusao = fields.String(required=False, description="data de exclusao")