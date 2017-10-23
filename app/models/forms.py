from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField("username", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	remember_me = BooleanField("remember_me")

class CadastroUser(FlaskForm):
	nome = StringField("nome", validators=[DataRequired()])
	email = StringField("email", validators=[DataRequired()])	
	username = StringField("username", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	tipo_u = StringField("tipo_u", validators=[DataRequired()])
	
class CadastroInstituicao(FlaskForm):
	nome = StringField("nome", validators=[DataRequired()])
	descricao = StringField("descricao", validators=[DataRequired()])
	id_u = StringField("id_u", validators=[DataRequired()])
	tipo_i = StringField("tipo_i", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	username = StringField("username", validators=[DataRequired()])

class CadastroEnderecoIns(FlaskForm):
	rua = StringField("rua", validators=[DataRequired()])
	numero = StringField("numero", validators=[DataRequired()])
	bairro = StringField("bairro", validators=[DataRequired()])
	cep = StringField("cep", validators=[DataRequired()])
	cidade = StringField("cidade", validators=[DataRequired()])
	estado = StringField("estado", validators=[DataRequired()])
	pais = StringField("pais", validators=[DataRequired()])
	latitude = StringField("latitude", validators=[DataRequired()])
	longitude = StringField("longitude", validators=[DataRequired()])

class InformarDoacao(FlaskForm):
	descricao = StringField("descricao", validators=[DataRequired()])
	data = StringField("data", validators=[DataRequired()])
	id_td = StringField("id_td", validators=[DataRequired()])
	
class DigitandoInstituicao(FlaskForm):
	tipo_i = StringField("tipo_i", validators=[DataRequired()])
