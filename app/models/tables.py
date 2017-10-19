from app import db

class TipoUsuario(db.Model):
	__tablename__ = "tipo_usuarios"

	id_tu = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String)

	def __init__(self, nome):
		self.nome = nome

	def __repr__(self):
		return "<Tipo do Usuário %r>" % self.nome

class Usuario(db.Model):
	__tablename__ = "usuarios"

	id_u = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String)
	email = db.Column(db.String, unique=True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	tipo_u = db.Column(db.Integer, db.ForeignKey('tipo_usuarios.id_tu'))

	tipo = db.relationship('TipoUsuario', foreign_keys = tipo_u)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id_u)

	def __init__(self, nome, email, username, password, tipo_u):
		self.nome = nome
		self.email = email
		self.username = username
		self.password = password
		self.tipo_u = tipo_u

	def __repr__(self):
		return "<User %r>" % self.username
	
	

class TipoInstituicao(db.Model):
	__tablename__ = "tipo_instituicoes"

	id_ti = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String)

	def __init__(self, nome):
		self.nome = nome

	def __repr__(self):

		return "<Tipo da Instituição %r>" % self.nome

class Instituicao(db.Model):
	__tablename__ = "instituicoes"

	id_i = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String)
	descricao = db.Column(db.String)
	id_u = db.Column(db.Integer, db.ForeignKey('usuarios.id_u'))
	tipo_i = db.Column(db.Integer, db.ForeignKey('tipo_instituicoes.id_ti'))
	password = db.Column(db.String)	
	username = db.Column(db.String, unique=True)
	
	usuario = db.relationship('Usuario', foreign_keys = id_u)
	tipo = db.relationship('TipoInstituicao', foreign_keys = tipo_i)
	
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id_i)

	def __init__(self, nome, descricao, id_u, tipo_i, password, username):
		self.nome = nome
		self.descricao = descricao
		self.id_u = id_u
		self.tipo_i = tipo_i
		self.password = password
		self.username = username

	def __repr__(self):
		return "<User %r>" % self.username

class Avaliacao(db.Model):
	__tablename__ = "avaliacoes"

	id_a = db.Column(db.Integer, primary_key=True)
	pontuacao = db.Column(db.Integer)
	comentario = db.Column(db.String)
	data = db.Column(db.String)
	id_u = db.Column(db.Integer, db.ForeignKey('usuarios.id_u'))
	id_i = db.Column(db.Integer, db.ForeignKey('instituicoes.id_i'))

	usuario = db.relationship('Usuario', foreign_keys = id_u)
	instituicao = db.relationship('Instituicao', foreign_keys = id_i)

	def __init__(self, pontuacao, comentario, data, id_u, id_i):
		self.pontuacao = pontuacao
		self.comentario = comentario
		self.data = data
		self.id_u = id_u
		self.id_i = id_i

	def __repr__(self):
		return "<Pontuação da avaliação %r>" % self.pontuacao

class EnderecoInstituicao(db.Model):
	__tablename__ = "endereco_instituicoes"

	id_ei = db.Column(db.Integer, primary_key=True)
	rua = db.Column(db.String)
	numero = db.Column(db.String)
	bairro = db.Column(db.String)
	cep = db.Column(db.String)
	cidade = db.Column(db.String)
	estado = db.Column(db.String)
	pais = db.Column(db.String)
	latitude = db.Column(db.String)
	longitude = db.Column(db.String)
	id_i = db.Column(db.Integer, db.ForeignKey('instituicoes.id_i'))

	instituicao = db.relationship('Instituicao', foreign_keys = id_i)

	def __init__(self, rua, numero, bairro, cep, cidade, estado, pais, latitude, longitude, id_i):
		self.rua = rua
		self.numero = numero
		self.bairro = bairro
		self.cep = cep
		self.cidade = cidade
		self.estado = estado
		self.pais = pais
		self.latitude = latitude
		self.longitude = longitude
		self.id_i = id_i

	def __repr__(self):
		return "<Endereço das instituições %r>" % self.rua
 
class TagsDoacao(db.Model):
	__tablename__ = "tags_doacao"
	
	id_td = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String)

	def __init__(self, tag):
		self.tag = tag

	def __repr__(self):
		return "<Tag %r>" % self.tag

class Doacao(db.Model):
	__tablename__ = "doacao"
	
	id_d = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String)
	data = db.Column(db.String)
	id_i = db.Column(db.Integer, db.ForeignKey('instituicoes.id_i'))
	id_td = db.Column(db.Integer, db.ForeignKey('tags_doacao.id_td'))

	instituicao = db.relationship('Instituicao', foreign_keys = id_i)
	tag = db.relationship('TagsDoacao', foreign_keys = id_td)

	def __init__(self, descricao, data, id_i, id_td):
		self.descricao = descricao
		self.data = data
		self.id_i = id_i
		self.id_td = id_td

	def __repr__(self):
		return "<Doação %r>" % self.descricao

class Denuncia(db.Model):
	__tablename__ = "denuncia"

	id_den = db.Column(db.Integer, primary_key=True)
	id_u = db.Column(db.Integer, db.ForeignKey('usuarios.id_u'))
	id_i = db.Column(db.Integer, db.ForeignKey('instituicoes.id_i'))
	descricao = db.Column(db.String)
	data = db.Column(db.String)

	usuario = db.relationship('Usuario', foreign_keys = id_u)
	instituicao = db.relationship('Instituicao', foreign_keys = id_i)

	def __init__(self, descricao, data):
		self.descricao = descricao
		self.data = data

	def __repr__(self):
		return "<Denuncia %r>" % self.descricao
