from .rdb import db

class EnderecosCliente(db.Model):

    __tablename__ = 'enderecosClientes'  # Real table name, since is case sensitive
    id = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer, nullable=False)
    CEP = db.Column(db.String,nullable=False)
    estado = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    logradouro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    
   

    def __init__(
                self,
                estado,
                CEP,
                cidade,
                logradouro,
                numero,
                idCliente,
            ):
        """Constructor to help write data"""

        self.estado = estado
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.numero = numero
        self.idCliente = idCliente


    def __repr__(self) -> str:
        """Object representation"""
        return self.estado
