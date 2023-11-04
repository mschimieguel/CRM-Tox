from .rdb import db

class Cliente(db.Model):

    __tablename__ = 'clientes'  # Real table name, since is case sensitive

    id = db.Column(db.Integer, primary_key=True)
    CPF_CNPJ = db.Column(db.String,nullable=True,unique=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    telefone = db.Column(db.String, nullable=True)
    whatsapp = db.Column(db.String, nullable=True)
    celular = db.Column(db.String, nullable=True)
    dataExclusao = db.Column(db.DateTime, nullable=True)
    dataNascimento = db.Column(db.DateTime, nullable=True)

    def __init__(
                self,
                nome,
                CPF_CNPJ=None,
                email=None,
                telefone=None,
                whatsapp=None,
                celular=None,
                dataExclusao=None,
                dataNascimento=None
            ):
        """Constructor to help write data"""

        self.nome = nome
        self.CPF_CNPJ = CPF_CNPJ
        self.email = email
        self.telefone = telefone
        self.whatsapp = whatsapp
        self.celular = celular
        self.dataExclusao = dataExclusao
        self.dataNascimento = dataNascimento

    def __repr__(self) -> str:
        """Object representation"""
        return self.nome
