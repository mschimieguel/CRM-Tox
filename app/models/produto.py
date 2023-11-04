from .rdb import db

class Produto(db.Model):

    __tablename__ = 'produtos'  # nome real da tabela (Case Sensitive)
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    codigoBarras = db.Column(db.String,nullable=True,unique=True)
    idFornecedor = db.Column(db.String,nullable=True,unique=True)

    def __init__(
                self, 
                 nome, 
                 codigoBarras,
                 idFornecedor
                 ) -> None:
        
        self.nome = nome
        self.codigoBarras = codigoBarras
        self.idFornecedor = idFornecedor

    def __repr__(self) -> str:
        """Object representation"""
        return self.nome
