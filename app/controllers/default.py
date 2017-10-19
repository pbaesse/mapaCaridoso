from flask import render_template, flash, redirect, url_for, request
from app import app, db, lm
from flask_login import login_user, logout_user, current_user
from app.models.forms import LoginForm, CadastroUser, CadastroInstituicao
from app.models.tables import Usuario, Instituicao

#<----- logar usuário e instituição e deslogar ------->

@lm.user_loader
def load_user(id_u):
	return Usuario.query.filter_by(id_u = id_u).first()

@lm.user_loader
def load_user(id_i):
	return Instituicao.query.filter_by(id_i = id_i).first()

@app.route("/loginu", methods=["GET","POST"])
def loginu():
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuario.query.filter_by(username=form.username.data).first()
		if user and user.password == form.password.data:
			login_user(user)
			flash("	Olá, "+user.nome+"!")
			return redirect(url_for("index"))
		else:
			flash("Login inválido!")
	return render_template('loginu.html',
			       form=form)

@app.route("/logini", methods=["GET","POST"])
def logini():
	form = LoginForm()
	if form.validate_on_submit():
		instituicao = Instituicao.query.filter_by(username=form.username.data).first()
		if instituicao and instituicao.password == form.password.data:
			login_user(instituicao)
			flash("	Olá, "+instituicao.nome+"!")
			return redirect(url_for("index"))
		else:
			flash("Login inválido!")
	return render_template('logini.html',
			       form=form)

@app.route("/logout")
def logout():
	logout_user()
	flash("Muito obrigado por sua visita. Até breve!")
	return redirect(url_for("index"))

@app.route("/quallogin")
def quallogin():
	return redirect(url_for("quallogar"))

@app.route("/quallogar")
def quallogar():
	return render_template('quallogin.html')

@app.route("/logarinstituicao")
def logarinstituicao():
	form = LoginForm()
	return render_template('logini.html', form=form)

@app.route("/logaruser")
def logaruser():
	form = LoginForm()
	return render_template('loginu.html', form=form)

#<----- logar usuário e instituição e deslogar ------->

#<----- cadastrar usuário e instituição e deslogar ------->

@app.route("/qualcadastro")
def qualcadastro():
	return redirect(url_for("qualcadastrar"))

@app.route("/qualcadastrar")
def qualcadastrar():
	return render_template('qualcadastro.html')

@app.route("/cadastraruser")
def cadastraruser():
	form = CadastroUser()
	return render_template('cadastrou.html', form=form)

@app.route("/cadastrou", methods=['GET', 'POST'])
def cadastrou():
	form = CadastroUser()
	if form.validate_on_submit():
		if request.method == "POST":
			nome =  request.form.get("nome")
			email = request.form.get("email")
			username = request.form.get("username")
			password = request.form.get("password")
			tipo_u = request.form.get("tipo_u")

			if nome and email and username and password and tipo_u:
				p = Usuario(nome, email, username, password, tipo_u)
				db.session.add(p)
				db.session.commit()

			return redirect(url_for("index"))
	return render_template('index.html',
					form=form)

@app.route("/cadastrarinstituicao")
def cadastrarinstituicao():
	form = CadastroInstituicao()
	return render_template('cadastroi.html', form=form)

@app.route("/cadastroi", methods=['GET', 'POST'])
def cadastroi():
	form = CadastroInstituicao()
	if form.validate_on_submit():
		if request.method == "POST":
			nome =  request.form.get("nome")
			descricao =  request.form.get("descricao")
			id_u = request.form.get("id_u")
			tipo_i = request.form.get("tipo_i")
			password = request.form.get("password")
			username = request.form.get("username")

			if nome and descricao and id_u and tipo_i and password and username:
				i = Instituicao(nome, descricao, id_u, tipo_i, password, username)
				db.session.add(i)
				db.session.commit()

			return redirect(url_for("index"))
	return render_template('index.html',
					form=form)

#<----- cadastrar usuário e instituição e deslogar ------->
@app.route("/index")
@app.route("/")
def index():
	return render_template('index.html')

