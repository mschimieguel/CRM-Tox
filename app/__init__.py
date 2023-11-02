from flask import Flask, render_template
from flask_restx import Api,Namespace, Resource, fields
from flask_marshmallow import Marshmallow
import os
from flask import Flask, render_template, request, url_for, redirect,jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
ma = Marshmallow()
basedir = os.getcwd()
print("basedir =============================")
print(basedir)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api()

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
    
    def __repr__(self):
        return f'<Grupo {self.firstname}>'

class GrupoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grupos
        load_instance = True

    nome = fields.String(required=True, description="Nome Grupo")
    fonte = fields.String(required=False, description="fonte de dados")
    

@api.route('/grupo', methods=['GET'])
class GrupoResource(Resource):
    def get(self):
        return listarTodosGrupos()
    
   
    
def listarTodosGrupos():
    result = Grupos.query.all()
    return GrupoSchema(many=True).jsonify(result)
