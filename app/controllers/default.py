from flask import render_template, flash, redirect, url_for, request, session
from app import app, db, lm
from datetime import datetime
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps
from flask_login import login_user, logout_user, current_user
from app.models.forms import LoginForm, CadastroUser, CadastroInstituicao, CadastroEnderecoIns, InformarDoacao, DigitandoInstituicao, DigitandoInstituicaoDoacao, AvaliarInstituicao, DenunciarInstituicao
from app.models.tables import Usuario, Instituicao, EnderecoInstituicao, Doacao, Avaliacao, Denuncia, TipoInstituicao, TagsDoacao, Administrador

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# you can also pass key here
GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")

#<----- logar usuário e instituição e deslogar ------->

@lm.user_loader
def load_user(id_u):
	return Usuario.query.filter_by(id_u = id_u).first()
def load_user(id_i):
	return Instituicao.query.filter_by(id_i = id_i).first()
def load_user(id_ad):
	return Administrador.query.filter_by(id_ad = id_ad).first()

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

@app.route("/logaradm")
def logaradm():
	form = LoginForm()
	return render_template('logina.html', form=form)

@app.route("/logaruser")
def logaruser():
	form = LoginForm()
	return render_template('loginu.html', form=form)

@app.route("/contatogeral")
def contatogeral():
	return render_template('contatogeral.html')

@app.route("/sobre")
def sobre():
	return render_template('sobre.html')

@app.route("/mapacaridoso")
def mapacaridoso():
	return render_template('mapacaridoso.html')

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
				return render_template('cadastrouok.html')
			return render_template('cadastrouinvalido.html')				
	return render_template('cadastrouinvalido.html', form=form)

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
			tipo_i = request.form.get("tipo_i")
			password = request.form.get("password")
			username = request.form.get("username")

			if nome and descricao and tipo_i and password and username:
				i = Instituicao(nome, descricao, tipo_i, password, username)
				db.session.add(i)
				db.session.commit()
				instituicao = Instituicao.query.filter_by(username=form.username.data).first()
				session['id_i']=instituicao.id_i
				return redirect(url_for("cadastrarenderecoins"))
			return render_template('cadastroiinvalido.html', form=form)		
		return render_template('cadastroiinvalido.html', form=form)
	return render_template('cadastroiinvalido.html',
					form=form)

#<----- cadastrar usuário e instituição e deslogar ------->

#<--------------- Instituições --------------------------->


@app.route("/direcionamentosi")
def direcionamentosi():
	return render_template('direcionamentosi.html')

@app.route("/perfilins", methods=['GET', 'POST'])
def perfilins():
	id = session['id_i']
	ins = Instituicao.query.filter_by(id_i=id).first()
	end = EnderecoInstituicao.query.filter_by(id_i=id).first()
	ava = Avaliacao.query.filter_by(id_i=id).all()
	doa = Doacao.query.filter_by(id_i=id).all()
	return render_template('perfilins.html', ins=ins, end=end, ava=ava, doa=doa)

@app.route("/cadastrarenderecoins")
def cadastrarenderecoins():
	form = CadastroEnderecoIns()
	return render_template('cadastrarenderecoins.html', 
						          form=form)

@app.route("/cadastroendereco", methods=['GET', 'POST'])
def cadastroendereco():
	form = CadastroEnderecoIns()
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
			id_i = session['id_i']

			if rua and numero and bairro and cep and cidade and estado and pais and latitude and longitude and id_i:
				c = EnderecoInstituicao(rua, numero, bairro, cep, cidade, estado, pais, latitude, longitude, id_i)
				db.session.add(c)
				db.session.commit()
				return render_template("cadastroiok.html")
			return render_template("cadastroenderecoinsinvalido.html", form=form)
		return render_template("cadastroenderecoinsinvalido.html", form=form)
	return render_template("cadastroenderecoinsinvalido.html", form=form)


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
	ins = session['id_i']
	now = datetime.now()
	if form.validate_on_submit():
		if request.method == "POST":
			descricao = request.form.get("descricao")
			dia = now.day
			mes = now.month
			ano = now.year
			id_i = ins
			id_td = session['id_td']
	
			if descricao and dia and mes and ano and id_i and id_td:
				ind = Doacao(descricao, dia, mes, ano, id_i, id_td)
				db.session.add(ind)
				db.session.commit()
				
				return render_template('informardoacaook.html')
			return redirect(url_for("informardoacao"))
	return render_template('informardoacaoins.html', form = form)


@app.route("/enderecoscadastrados")
def enderecoscadastrados():
	ins = session['id_i']
	endereco_instituicoes = EnderecoInstituicao.query.filter_by(id_i=ins).all()
	return render_template("enderecoscadastrados.html", endereco_instituicoes=endereco_instituicoes)

@app.route("/doacoescadastradas")
def doacoescadastradas():
	ins = session['id_i']
	doacao = Doacao.query.filter_by(id_i=ins).all()
	return render_template("doacoescadastradas.html", doacao=doacao)

@app.route("/avaliacoesfeitas")
def avaliacoesfeitas():
	ins = session['id_i']
	ava = Avaliacao.query.filter_by(id_i=ins).all()
	return render_template("avafeitas.html", ava=ava)

@app.route("/excluirdoacoes1/<int:id>", methods=['GET'])
def excluirdoacoes1(id):
	doa = Doacao.query.filter_by(id_d=id).first()
	db.session.delete(doa)
	db.session.commit()

	return redirect(url_for("doacoescadastradas"))

@app.route("/excluirdoacoes2/<int:id>", methods=['GET'])
def excluirdoacoes2(id):
	doa = Doacao.query.filter_by(id_d=id).first()
	db.session.delete(doa)
	db.session.commit()

	return redirect(url_for("perfilins"))
#<--------------- Instituições --------------------------->

#<------------------ Usuário ----------------------------->
@app.route("/direcionamentosu")
def direcionamentosu():
	return render_template('direcionamentosu.html')

@app.route("/perfilusu", methods=['GET', 'POST'])
def perfilusu():
	id = current_user.id_u
	ava = Avaliacao.query.filter_by(id_u=id).all()
	den = Denuncia.query.filter_by(id_u=id).all()
	usu = Usuario.query.filter_by(id_u=id).first()
	return render_template('perfilusu.html', usu=usu, ava=ava, den=den)

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
	end = EnderecoInstituicao.query.filter_by(id_i=id).first()
	ava = Avaliacao.query.filter_by(id_i=id).all()
	den = Denuncia.query.filter_by(id_i=id).all()
	doa = Doacao.query.filter_by(id_i=id).all()
	return render_template("instituicoesencontradasdoacoes.html", ins=ins, end=end, ava=ava, den=den, doa=doa)

@app.route("/buscarendereco/", methods=['GET'])
def buscarendereco():
	id_i = EnderecoInstituicao.query.all()
	return render_template("enderecosencontradosdoacoes.html", id_i=id_i)
			

@app.route("/avaliarins/", methods=['GET', 'POST'])
def avaliarins():
	form = AvaliarInstituicao()
	ins = Instituicao.query.all()
	return render_template('avaliarins.html', ins=ins, form=form)

@app.route("/avaliarinst/<int:id>", methods=['GET'])
def avaliarinst(id):
	form = AvaliarInstituicao()
	session['id_i'] = id
	session['nome_i'] = Instituicao.query.filter_by(id_i=id).first().nome	
	ins = Instituicao.query.all()
	return render_template('avaliarinstituicao.html', ins=ins, form=form)

@app.route("/avaliarinstituicao/", methods=['GET', 'POST'])
def avaliarinstituicao():
	form = AvaliarInstituicao()
	usu = current_user.id_u
	now = datetime.now()
	if form.validate_on_submit():
		if request.method == "POST":			
			id_u = usu		
			id_i = session['id_i']
			pontuacao = request.form.get("pontuacao")
			comentario = request.form.get("comentario")
			dia = now.day
			mes = now.month
			ano = now.year
	
			if id_u and id_i and pontuacao and comentario and dia and mes and ano:
				ava = Avaliacao(id_u, id_i, pontuacao, comentario, dia, mes, ano)
				db.session.add(ava)
				db.session.commit()
			
				return render_template('avaliarinstituicaook.html')
			return redirect(url_for("avaliarinstituicao"))
	return render_template('paginainicialusu.html', form = form)		

@app.route("/denunciarins", methods=['GET', 'POST'])
def denunciarins():
	form = DenunciarInstituicao()
	ins = Instituicao.query.all()
	return render_template('denunciarins.html', ins=ins, form=form)

@app.route("/denunciarinst/<int:id>", methods=['GET'])
def denunciarinst(id):
	form = DenunciarInstituicao()
	session['id_i']=id
	session['nome_i'] = Instituicao.query.filter_by(id_i=id).first().nome	
	ins = Instituicao.query.all()
	return render_template('denunciarinstituicao.html', ins=ins, form=form)

@app.route("/denunciarinstituicao", methods=['GET', 'POST'])
def denunciarinstituicao():
	form = DenunciarInstituicao()
	usu = current_user.id_u
	now = datetime.now()
	if form.validate_on_submit():
		if request.method == "POST":
			id_u = usu
			id_i = session['id_i']
			descricao = request.form.get("descricao")
			dia = now.day
			mes = now.month
			ano = now.year

			if id_u and id_i and descricao and dia and mes and ano:
				den = Denuncia(id_u, id_i, descricao, dia, mes, ano)
				db.session.add(den)
				db.session.commit()

				return render_template('denunciarinstituicaook.html')
			return redirect(url_for("denunciarinstituicao"))
	return render_template('paginainicialusu.html', form = form)		

@app.route("/excluirdenuncia1/<int:id>", methods=['GET'])
def excluirdenuncia1(id):
	den = Denuncia.query.filter_by(id_den=id).first()
	db.session.delete(den)
	db.session.commit()

	return redirect(url_for("perfilusu"))

@app.route("/excluiravaliacoes1/<int:id>", methods=['GET'])
def excluiravaliacoes1(id):
	ava = Avaliacao.query.filter_by(id_a=id).first()
	db.session.delete(ava)
	db.session.commit()

	return redirect(url_for("perfilusu"))
#<----------------ADM-------------->
@app.route("/perfiladm", methods=['GET', 'POST'])
def perfiladm():
	id = session['id_ad']
	adm = Administrador.query.filter_by(id_ad=id).first()
	return render_template('perfiladm.html', adm=adm)

@app.route("/direcionamentos")
def direcionamentos():
	return render_template('direcionamentos.html')

@app.route("/visualizardenuncias/", methods=['GET'])
def visualizardenuncias():
	den = Denuncia.query.all()
	return render_template("denunciasencontradas.html", den=den)

@app.route("/visualizaravaliacoes/")
def visualizaravaliacoes():
	ava = Avaliacao.query.all()
	return render_template("avaliacoesrealizadas.html", ava=ava)

@app.route("/visualizardoacoes/")
def visualizardoacoes():
	doa = Doacao.query.all()
	return render_template("doacoesrealizadas.html", doa=doa)

@app.route("/visualizarinstituicoes1/")
def visualizarinstituicoes1():
	ins = Instituicao.query.all()
	return render_template("instituicoescadastradas.html", ins=ins)

@app.route("/visualizardoadores1/")
def visualizardoadores1():
	usu = Usuario.query.all()
	return render_template("usuarioscadastrados.html", usu=usu)

@app.route("/visualizarinstituicoes/<int:id>", methods=['GET'])
def visualizarinstituicoes(id):
	ins = Instituicao.query.filter_by(id_i=id).first()
	end = EnderecoInstituicao.query.filter_by(id_i=id).first()
	ava = Avaliacao.query.filter_by(id_i=id).all()
	doa = Doacao.query.filter_by(id_i=id).all()
	den = Denuncia.query.filter_by(id_i=id).all()
	return render_template("visualizarinstituicoes.html", ins=ins, end=end, ava=ava, doa=doa, den=den)

@app.route("/excluirinstituicoes", methods=['GET'])
def excluirinstituicoes():
	ava = session['id_i']
	end = EnderecoInstituicao.query.filter_by(id_i=ava).first()
	db.session.delete(end)
	db.session.commit()
	ins = Instituicao.query.filter_by(id_i=ava).first()
	db.session.delete(ins)
	db.session.commit()

	return render_template("excluirinstituicoes.html")

@app.route("/excluirdenuncia/<int:id>", methods=['GET'])
def excluirdenuncia(id):
	den = Denuncia.query.filter_by(id_den=id).first()
	db.session.delete(den)
	db.session.commit()

	return redirect(url_for("visualizardenuncias"))

@app.route("/excluiravaliacoes/<int:id>", methods=['GET'])
def excluiravaliacoes(id):
	ava = Avaliacao.query.filter_by(id_a=id).first()
	db.session.delete(ava)
	db.session.commit()

	return redirect(url_for("visualizaravaliacoes"))

@app.route("/excluirdoacoes/<int:id>", methods=['GET'])
def excluirdoacoes(id):
	doa = Doacao.query.filter_by(id_d=id).first()
	db.session.delete(doa)
	db.session.commit()

	return redirect(url_for("visualizardoacoes"))

@app.route("/visualizardoadores/<int:id>", methods=['GET'])
def visualizardoadores(id):
	usu = Usuario.query.filter_by(id_u=id).first()
	ava = Avaliacao.query.filter_by(id_u=id).all()
	den = Denuncia.query.filter_by(id_u=id).all()
	return render_template("visualizardoadores.html", usu=usu, ava=ava, den=den)

@app.route("/testando/<int:id>", methods=['GET'])
def testando(id):
	session['id'] = id
	return render_template("testando.html")

@app.route("/testando1/<int:id>", methods=['GET'])
def testando1(id):
	session['id_i'] = id
	return render_template("testando1.html")

@app.route("/excluirdoadores/", methods=['GET'])
def excluirdoadores():
	ava = session['id']
	usu = Usuario.query.filter_by(id_u=ava).first()
	db.session.delete(usu)
	db.session.commit()

	return render_template("excluirdoadores.html")



#<--------------------------------------------------------GOOGLE MAPS-------------------------------------------------------------------------->
@app.route("/index")
@app.route("/")
def index():
    trdmap = Map(
        identifier="trdmap",
        lat=-5.633859,
        lng=-35.425515,
	style="height:500px;width:1140px;margin:0;",
        markers=[
            {
                'icon': '../static/images/heart.png',
                'lat': 	-5.633859,
                'lng':  -35.425515,
                'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais! - Necessitamos de roupas para crianças de até 10 anos de idade e materiais de limpeza."
            },
            {
                'icon': '../static/images/heart.png',
                'lat':	-5.646472,
                'lng':	-35.42082,
                'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim - Necessitamos de materiais de limpeza.")
            },
              {
                'icon': '../static/images/heart.png',
                'lat':	-5.634113,
                'lng':	-35.42502,
                'infobox': ("Igreja Matriz de Nossa Senhora da Conceição - Necessitamos de materiais de limpeza.")
            },
	    {
                'icon': '../static/images/heart.png',
                'lat':	-5.638723,
                'lng':	-35.426966,
                'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
            },
        ]
    )
    return render_template('index.html', trdmap=trdmap)

@app.route("/paginainicialusu")
def paginainicialusu():
	trdmap = Map(
	identifier="trdmap",
	lat=-5.633859,
	lng=-35.425515,
	style="height:550px;width:1060px;margin:0;",
	markers=[
	{
	'icon': '../static/images/heart.png',
	'lat': 	-5.633859,
	'lng':  -35.425515,
	'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.646472,
	'lng':	-35.42082,
	'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.634113,
	'lng':	-35.42502,
	'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.638723,
	'lng':	-35.426966,
	'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
	},
	]
	)
	return render_template('paginainicialusu.html', trdmap=trdmap)

@app.route("/paginainicialins")
def paginainicialins():
	trdmap = Map(
	identifier="trdmap",
	lat=-5.633859,
	lng=-35.425515,
	style="height:550px;width:1060px;margin:0;",
	markers=[
	{
	'icon': '../static/images/heart.png',
	'lat': 	-5.633859,
	'lng':  -35.425515,
	'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.646472,
	'lng':	-35.42082,
	'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.634113,
	'lng':	-35.42502,
	'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.638723,
	'lng':	-35.426966,
	'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
	},
	]
	)
	return render_template('paginainicialins.html', trdmap=trdmap)

@app.route("/paginainicialadm")
def paginainicialadm():
	trdmap = Map(
	identifier="trdmap",
	lat=-5.633859,
	lng=-35.425515,
	style="height:550px;width:1060px;margin:0;",
	markers=[
	{
	'icon': '../static/images/heart.png',
	'lat': 	-5.633859,
	'lng':  -35.425515,
	'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.646472,
	'lng':	-35.42082,
	'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.634113,
	'lng':	-35.42502,
	'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
	},
	{
	'icon': '../static/images/heart.png',
	'lat':	-5.638723,
	'lng':	-35.426966,
	'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
	},
	]
	)
	return render_template('paginainicialadm.html', trdmap=trdmap)


@app.route("/logina", methods=["GET","POST"])
def logina():
	form = LoginForm()
	if form.validate_on_submit():
		adm = Administrador.query.filter_by(username=form.username.data).first()
		if adm and adm.password == form.password.data:
			login_user(adm)
			session['id_ad']=adm.id_ad
			session['nome_u']=adm.nome
			trdmap = Map(
			identifier="trdmap",
			lat=-5.633859,
			lng=-35.425515,
			style="height:550px;width:1060px;margin:0;",
			markers=[
			{
			'icon': '../static/images/heart.png',
			'lat': 	-5.633859,
			'lng':  -35.425515,
			'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.646472,
			'lng':	-35.42082,
			'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.634113,
			'lng':	-35.42502,
			'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.638723,
			'lng':	-35.426966,
			'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
			},
			]
			)
			return render_template('paginainicialadm.html', trdmap=trdmap)
		else:
			return render_template('loginainvalido.html', form=form)
	return render_template('loginainvalido.html',
			       form=form)

@app.route("/loginu", methods=["GET","POST"])
def loginu():
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuario.query.filter_by(username=form.username.data).first()
		if user and user.password == form.password.data:
			login_user(user)
			session['nome_u']=user.nome
			trdmap = Map(
			identifier="trdmap",
			lat=-5.633859,
			lng=-35.425515,
			style="height:550px;width:1060px;margin:0;",
			markers=[
			{
			'icon': '../static/images/heart.png',
			'lat': 	-5.633859,
			'lng':  -35.425515,
			'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.646472,
			'lng':	-35.42082,
			'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.634113,
			'lng':	-35.42502,
			'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.638723,
			'lng':	-35.426966,
			'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
			},
			]
			)
			return render_template('paginainicialusu.html', trdmap=trdmap)
		else:
			return render_template('loginuinvalido.html', form=form)
	return render_template('loginuinvalido.html',
			       form=form)

@app.route("/logini", methods=["GET","POST"])
def logini():
	form = LoginForm()
	if form.validate_on_submit():
		instituicao = Instituicao.query.filter_by(username=form.username.data).first()
		if instituicao and instituicao.password == form.password.data:
			login_user(instituicao)
			session['nome_i']=instituicao.nome
			session['id_i']=instituicao.id_i
			trdmap = Map(
			identifier="trdmap",
			lat=-5.633859,
			lng=-35.425515,
			style="height:550px;width:1060px;margin:0;",
			markers=[
			{
			'icon': '../static/images/heart.png',
			'lat': 	-5.633859,
			'lng':  -35.425515,
			'infobox': "APAE de Ceará-Mirim - Instituição que lida com pessoas com necessidas especiais!"
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.646472,
			'lng':	-35.42082,
			'infobox': ("Hospital Dr. Percílio Alves - Hospital público na cidade de Ceará-Mirim")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.634113,
			'lng':	-35.42502,
			'infobox': ("Igreja Matriz de Nossa Senhora da Conceição")
			},
			{
			'icon': '../static/images/heart.png',
			'lat':	-5.638723,
			'lng':	-35.426966,
			'infobox': ("Canários Rações - Microempresa especializada no mundo pet")
			},
			]
			)
			return render_template('paginainicialins.html', trdmap=trdmap)
		else:
			return render_template('loginiinvalido.html', form=form)
	return render_template('loginiinvalido.html',
			       form=form)
