from flask import render_template, flash, redirect, url_for, request, session
from app import app, db, lm
from flask_login import login_user, logout_user, current_user
from app.models.forms import LoginForm, CadastroUser, CadastroInstituicao, CadastroEnderecoIns, InformarDoacao, DigitandoInstituicao, DigitandoInstituicaoDoacao, AvaliarInstituicao, DenunciarInstituicao
from app.models.tables import Usuario, Instituicao, EnderecoInstituicao, Doacao, Avaliacao, Denuncia, TipoInstituicao, TagsDoacao

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
			session['nome_u']=user.nome;
			return render_template('paginainicialusu.html')
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
			session['nome_i']=instituicao.nome;
			return render_template('paginainicialins.html')
			
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
				instituicao = Instituicao.query.filter_by(username=form.username.data).first()
				login_user(instituicao)

			return redirect(url_for("cadastrarenderecoins"))
	return render_template('index.html',
					form=form)

#<----- cadastrar usuário e instituição e deslogar ------->

#<--------------- Instituições --------------------------->
@app.route("/paginainicialins")
def paginainicialins():
	ins = current_user.username
	return render_template('paginainicialins.html')

@app.route("/cadastrarenderecoins")
def cadastrarenderecoins():
	form = CadastroEnderecoIns()
	return render_template('cadastrarenderecoins.html', 
						          form=form)

@app.route("/cadastroendereco", methods=['GET', 'POST'])
def cadastroendereco():
	form = CadastroEnderecoIns()	
	ins = current_user.id_i
	if form.validate_on_submit():
		if request.method == "POST":
			rua = request.form.get("rua")
			numero = request.form.get("numero")
			bairro = request.form.get("bairro")
			cep = request.form.get("cep")
			cidade = request.form.get("cidade")
			estado = request.form.get("estado")
			pais = request.form.get("pais")
			latitude = request.form.get("latitude")
			longitude = request.form.get("longitude")
			id_i = ins

			if rua and numero and bairro and cep and cidade and estado and pais and latitude and longitude and id_i:
				c = EnderecoInstituicao(rua, numero, bairro, cep, cidade, estado, pais, latitude, longitude, id_i)
				db.session.add(c)
				db.session.commit()

			return redirect(url_for("paginainicialins"))
	return render_template('paginainicialins.html',form=form)


@app.route("/informardoacaoins")
def informardoacaoins():
	doa = TagsDoacao.query.all()
	form = InformarDoacao()
	return render_template('informardoacaoinstituicao.html', 
						          form=form, doa=doa)

@app.route("/informardoacaoinstituicao/<int:id>")
def informardoacaoinstituicao(id):
	form = InformarDoacao()
	session['id_td']=id
	return render_template('informardoacaoins.html', 
						          form=form)

@app.route("/informardoacao", methods=['GET', 'POST'])
def informardoacao():
	form = InformarDoacao()
	ins = current_user.id_i
	if form.validate_on_submit():
		if request.method == "POST":
			descricao = request.form.get("descricao")
			data = request.form.get("data")
			id_i = ins
			id_td = session['id_td']
	
			if descricao and data and id_i and id_td:
				ind = Doacao(descricao, data, id_i, id_td)
				db.session.add(ind)
				db.session.commit()

			return redirect(url_for("paginainicialins"))
	return render_template('paginainicialins.html', form = form)


@app.route("/enderecoscadastrados")
def enderecoscadastrados():
	ins = current_user.id_i
	endereco_instituicoes = EnderecoInstituicao.query.filter_by(id_i=ins).all()
	return render_template("enderecoscadastrados.html", endereco_instituicoes=endereco_instituicoes)

@app.route("/doacoescadastradas")
def doacoescadastradas():
	ins = current_user.id_i
	doacao = Doacao.query.filter_by(id_i=ins).all()
	return render_template("doacoescadastradas.html", doacao=doacao)

@app.route("/avaliacoesfeitas")
def avaliacoesfeitas():
	ins = current_user.id_i
	ava = Avaliacao.query.filter_by(id_i=ins).all()
	return render_template("avafeitas.html", ava=ava)
#<--------------- Instituições --------------------------->

#<------------------ Usuário ----------------------------->

@app.route("/paginainicialusu")
def paginainicialusu():
	return render_template('paginainicialusu.html')

@app.route("/digitandoinstituicao")
def digitandoinstituicao():
	form = DigitandoInstituicao()
	return render_template('digitandoinstituicao.html', form=form)

@app.route("/buscandoinstituicao/<int:id>", methods=['GET'])
def buscandoinstituicao(id):
	ins = Instituicao.query.filter_by(tipo_i=id).all()
	return render_template("instituicoesencontradas.html", ins=ins)

@app.route("/doacoesencontradas")
def doacoesencontradas():
	doacoes = Doacao.query.all()
	return render_template("doacoesencontradas.html", doacoes=doacoes)

@app.route("/tiposencontrados")
def tiposencontrados():
	tipos = TipoInstituicao.query.all()
	return render_template("digitandoinstituicao.html", tipos=tipos)

@app.route("/buscandoinstituicaodoacao/<int:id>", methods=['GET'])
def buscandoinstituicaodoacao(id):
	ins = Instituicao.query.filter_by(id_i=id).first()	
	onde = EnderecoInstituicao.query.filter_by(id_i=id).first()
	return render_template("instituicoesencontradasdoacoes.html", ins=ins, onde=onde)

@app.route("/buscarendereco/", methods=['GET'])
def buscarendereco():
	id_i = EnderecoInstituicao.query.all()
	return render_template("enderecosencontradosdoacoes.html", id_i=id_i)
			

@app.route("/avaliarins/", methods=['GET', 'POST'])
def avaliarins():
	usu = current_user.id_u
	form = AvaliarInstituicao()
	ins = Instituicao.query.all()
	return render_template('avaliarins.html', ins=ins, form=form)

@app.route("/avaliarinst/<int:id>", methods=['GET'])
def avaliarinst(id):
	usu = current_user.id_u
	form = AvaliarInstituicao()
	session['id_i']=id
	ins = Instituicao.query.all()
	return render_template('avaliarinstituicao.html', ins=ins, form=form)

@app.route("/avaliarinstituicao/", methods=['GET', 'POST'])
def avaliarinstituicao():
	form = AvaliarInstituicao()
	usu = current_user.id_u
	if form.validate_on_submit():
		if request.method == "POST":
			pontuacao = request.form.get("pontuacao")
			comentario = request.form.get("comentario")
			data = request.form.get("data")
			id_u = usu		
			id_i = session['id_i']
	
			if pontuacao and comentario and data and id_u and id_i:
				ava = Avaliacao(pontuacao, comentario, data, id_u, id_i)
				db.session.add(ava)
				db.session.commit()
			
			return redirect(url_for("avaliarinstituicao"))
	return render_template('paginainicialusu.html', form = form)		

@app.route("/denunciarins", methods=['GET', 'POST'])
def denunciarins():
	usu = current_user.id_u
	form = DenunciarInstituicao()
	ins = Instituicao.query.all()
	return render_template('denunciarins.html', ins=ins, form=form)

@app.route("/denunciarinst/<int:id>", methods=['GET'])
def denunciarinst(id):
	usu = current_user.id_u
	form = DenunciarInstituicao()
	session['id_i']=id
	ins = Instituicao.query.all()
	return render_template('denunciarinstituicao.html', ins=ins, form=form)

@app.route("/denunciarinstituicao", methods=['GET', 'POST'])
def denunciarinstituicao():
	form = DenunciarInstituicao()
	usu = current_user.id_u
	if form.validate_on_submit():
		if request.method == "POST":
			id_u = usu
			id_i = session['id_i']
			descricao = request.form.get("descricao")
			data = request.form.get("data")		

			if id_u and id_i and descricao and data:
				den = Denuncia(id_u, id_i, descricao, data)
				db.session.add(den)
				db.session.commit()
			
			return redirect(url_for("denunciarinstituicao"))
	return render_template('paginainicialusu.html', form = form)		
#<------------------ Usuário ----------------------------->
@app.route("/index")
@app.route("/")
def index():
	return render_template('index.html')





