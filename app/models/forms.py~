from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, RadioField, TextField
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
	tipo_u = SelectField('', choices=[('1', 'Anonimo'), ('2', 'Empresa Privada'), ('3', 'Empresa Pública'), ('4', 'Autonomo')])
	
class CadastroInstituicao(FlaskForm):
	nome = StringField("nome", validators=[DataRequired()])
	descricao = StringField("descricao", validators=[DataRequired()])
	tipo_i = SelectField('', choices=[('1', 'Família'), ('2', 'Escola'), ('3', 'Igreja'), ('4', 'Economica'), ('5', 'Política'), ('6', 'Lazer'), ('7', 'ONGS'), ('8', 'Animais'), ('9', 'Outros')])
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
	
class DigitandoInstituicao(FlaskForm):
	tipo_i = StringField("tipo_i", validators=[DataRequired()])

class DigitandoInstituicaoDoacao(FlaskForm):
	id_i = StringField("id_i", validators=[DataRequired()])

class AvaliarInstituicao(FlaskForm):
	pontuacao = RadioField('', choices = [('2','Muito ruim'),('4','Ruim'),('6','Mediano'),('8','Bom'),('10','Muito bom')])
	comentario = TextField("comentario", validators=[DataRequired()])

class DenunciarInstituicao(FlaskForm):
	descricao = StringField("descricao", validators=[DataRequired()])
