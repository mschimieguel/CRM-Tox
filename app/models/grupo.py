from .rdb import db

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