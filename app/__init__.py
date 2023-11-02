from flask import Flask, render_template
from flask_restx import Api,Namespace, Resource, fields
api = Api()
app = Flask(__name__)
api.init_app(app)
 
@api.route('/index', methods=['GET'])
class IndexResource(Resource):
    def get(self):
        return render_template("index.html")