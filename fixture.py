from models import Session, Action, General, Category, Subcategory, engine, Base

Base.metadata.create_all(engine)

session = Session()

# Actions
expenses = Action(name='expenses')
income = Action(name='income')
session.add(income)
session.commit()

session.add_all([expenses, income])
session.commit()

# Category
alimentacao = Category(name='alimentacao')
casa = Category(name='casa')
transporte = Category(name='transporte')
esporte = Category(name='esporte')
saude = Category(name='saude')
burocracia = Category(name='burocracia')
compras = Category(name='compras')
escritorio = Category(name='escritorio')
filho = Category(name='filho')
session.add_all([alimentacao, casa, transporte, esporte, saude, burocracia, compras, escritorio, filho])
session.commit()

# Subcategory
alimentacao = session.query(Category).filter_by(name='alimentacao').one()
restaurante = Subcategory(category_id=alimentacao.id, name='restaurante')
supermercado = Subcategory(category_id=alimentacao.id, name='supermercado')
feira = Subcategory(category_id=alimentacao.id, name='feira')
session.add_all([restaurante, supermercado, feira])
session.commit()

casa = session.query(Category).filter_by(name='casa').one()
internet = Subcategory(category_id=casa.id, name='internet')
luz = Subcategory(category_id=casa.id, name='luz')
condominio = Subcategory(category_id=casa.id, name='condominio')
telefone = Subcategory(category_id=casa.id, name='telefone')
aluguel = Subcategory(category_id=casa.id, name='aluguel')
manutencao = Subcategory(category_id=casa.id, name='manutencao')
session.add_all([internet, luz, condominio, telefone, aluguel, manutencao])
session.commit()

transporte = session.query(Category).filter_by(name='transporte').one()
onibus = Subcategory(category_id=transporte.id, name='onibus')
gasolina = Subcategory(category_id=transporte.id, name='gasolina')
taxi = Subcategory(category_id=transporte.id, name='taxi')
oficina = Subcategory(category_id=transporte.id, name='oficina')
pedagio = Subcategory(category_id=transporte.id, name='pedagio')
session.add_all([onibus, gasolina, taxi, oficina, pedagio])
session.commit()

esporte = session.query(Category).filter_by(name='esporte').one()
gym = Subcategory(category_id=esporte.id, name='gym')
session.add_all([gym])
session.commit()

saude = session.query(Category).filter_by(name='saude').one()
exames = Subcategory(category_id=saude.id, name='exames')
farmacia = Subcategory(category_id=saude.id, name='farmacia')
cabelereiro = Subcategory(category_id=saude.id, name='cabelereiro')
viagem = Subcategory(category_id=saude.id, name='viagem')
session.add_all([exames, farmacia, cabelereiro, viagem])
session.commit()

burocracia = session.query(Category).filter_by(name="burocracia").one()
monotributo = Subcategory(category_id=burocracia.id, name='monotributo')
session.add_all([monotributo])
session.commit()

escritorio = session.query(Category).filter_by(name="escritorio").one()
aluguel = Subcategory(category_id=escritorio.id, name='aluguel')
manutencao = Subcategory(category_id=escritorio.id, name='manutencao')
session.add_all([aluguel, manutencao])
session.commit()

escola = Subcategory(category_id=filho.id, name='escola')
session.add_all([escola])
session.commit()
