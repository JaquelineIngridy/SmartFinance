from flask import Flask, request, redirect, url_for, flash, render_template,jsonify
import re
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, login_user, current_user, UserMixin
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from datetime import datetime  # Importa datetime para validação de data
from flask_migrate import Migrate, upgrade
from datetime import datetime 






# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = (
    f"mssql+pyodbc://@{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Função para formatar valores como moeda
def format_currency(value):
    return f"R$: {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

# Registre o filtro customizado no ambiente do Jinja2
app.jinja_env.filters['format_currency'] = format_currency


# Configurar o serializador para gerar tokens
s = URLSafeTimedSerializer(app.secret_key)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Configuração do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da função de rota para o login

Base = declarative_base()

# Definindo o modelo Usuario
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    datanasc = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    senha = db.Column(db.String(255))

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Classe Conta Bancária
class Contabancaria(db.Model):
    __tablename__ = 'Contabancaria'
    id = db.Column(db.Integer, primary_key=True)
    nome_banco = db.Column(db.String(100), nullable=False)
    saldo_atual = db.Column(db.Float, nullable=False)
    tipo_conta = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', backref=db.backref('contas', lazy=True))

    def __init__(self, usuario_id, nome_banco, tipo_conta, saldo_atual):
        self.usuario_id = usuario_id
        self.nome_banco = nome_banco
        self.tipo_conta = tipo_conta
        self.saldo_atual = saldo_atual

    def __repr__(self):
        return f'<Conta {self.nome_banco}, Tipo: {self.tipo_conta}, Saldo: {self.saldo_atual}>'



# Função para carregar usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Rota index
@app.route('/')
def index():
    return render_template('login.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id  # Salvando o ID do usuário na sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('tela_principal'))  # Redireciona para a tela principal
        else:
            flash('E-mail ou senha incorretos. Tente novamente.', 'danger')

    return render_template('login.html')



# Rota para a tela principal
@app.route('/tela_principal')
@login_required
def tela_principal():
    # Obtém a hora atual para saudação
    hora_atual = datetime.now().hour
    if 6 <= hora_atual < 12:
        saudacao = "Bom dia"
    elif 12 <= hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"
    
    
    # Obtém o nome do usuário logado
    nome_usuario = current_user.nome
    # Obtém todas as contas do usuário logado
    contas_usuario = Contabancaria.query.filter_by(usuario_id=current_user.id).all()
    
    # Obter o resumo financeiro
    resumo = calcular_resumo_financeiro(usuario_id=current_user.id)
    
    usuario_id = current_user.id  # Obter ID do usuário logado
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).all()

    # Função para calcular os totais
    def calcular_saldo(contas_usuario):
        saldo_total = 0.0
        receita_total = 0.0
        despesa_total = 0.0
        
        # Suponha que você tenha lógica para diferenciar receita e despesa
        for conta in contas_usuario:
            saldo_total += conta.saldo_atual
            
            # Simulando lógica para receita/despesa (isso depende do seu modelo de negócio)
            if conta.tipo_conta.lower() == "corrente":  # Exemplo: se for conta corrente, somamos à receita
                receita_total += conta.saldo_atual
            elif conta.tipo_conta.lower() == "poupança":  # Se for poupança, somamos à despesa
                despesa_total += conta.saldo_atual
        
        return saldo_total, receita_total, despesa_total

    # Calculando os totais
    saldo_total, receita_total, despesa_total = calcular_saldo(contas_usuario)

    # Renderizar o template com os valores
    return render_template('tela_principal.html', 
                           usuario=current_user, 
                           saudacao=saudacao, 
                           contas=contas_usuario, 
                            receita_total=resumo['receita_total'],
                            despesa_total=resumo['despesa_total'], 
                           saldo_total=resumo['balanco'],
                           nome_usuario=nome_usuario, 
                           transacoes=transacoes)


def calcular_resumo_financeiro(usuario_id):
    # Consultar soma das receitas e despesas
    receita_total = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.tipo == 'receita',
        Transacao.usuario_id == usuario_id
    ).scalar() or 0

    despesa_total = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.tipo == 'despesa',
        Transacao.usuario_id == usuario_id
    ).scalar() or 0

    # Calcular o balanço
    balanco = receita_total - despesa_total

    return {
        'receita_total': receita_total,
        'despesa_total': despesa_total,
        'balanco': balanco
    }



def calcular_totais_por_transacao(transacoes):
    receita_total = sum(t.valor for t in transacoes if t.tipo.lower() == "receita")
    despesa_total = sum(t.valor for t in transacoes if t.tipo.lower() == "despesa")
    saldo_total = receita_total - despesa_total
    return saldo_total, receita_total, despesa_total


@app.route('/atualizar_dados', methods=['POST'])
@login_required
def atualizar_dados():
    try:
        # Obter transações do usuário
        transacoes_usuario = Transacao.query.filter_by(usuario_id=current_user.id).all()
        
        # Calcular os totais
        saldo_total, receita_total, despesa_total = calcular_totais_por_transacao(transacoes_usuario)
        
        return jsonify({
            'success': True,
            'message': 'Dados atualizados com sucesso!',
            'saldo_total': saldo_total,
            'receita_total': receita_total,
            'despesa_total': despesa_total
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        datanasc = request.form['datanasc']
        sexo = request.form['sexo']
        senha = generate_password_hash(request.form['senha'])  # Gerando o hash da senha

        # Validação do e-mail para ser do Gmail
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            flash('O e-mail deve ser um endereço do Gmail (exemplo: usuario@gmail.com)', 'error')
            return render_template('cadastro.html')

        # Validação de comprimento da senha
        if len(request.form['senha']) < 6:
            flash('A senha deve ter pelo menos 6 caracteres!', 'error')
            return render_template('cadastro.html')

        # Validação de data
        try:
            datetime.strptime(datanasc, '%Y-%m-%d')
        except ValueError:
            flash('Data de nascimento inválida. Use o formato AAAA-MM-DD.', 'error')
            return render_template('cadastro.html')

        # Inserindo o novo usuário no banco de dados
        novo_usuario = Usuario(nome=nome, email=email, cpf=cpf, datanasc=datanasc, sexo=sexo, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

#acessoLogin rota
@app.route('/acessoLogin', methods=['POST'])
def acesso_login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.senha, senha):
        login_user(usuario)  # Loga o usuário
        return redirect(url_for('tela_principal'))
    else:
        print('E-mail ou senha incorretos.')
        return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))



# Modelo da tabela Transacao
class Transacao(db.Model):
    __tablename__ = 'Transacao'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    metodo_pagamento = db.Column(db.String(100), nullable=False)
    notas = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

from flask import session

@app.route('/transacoes')
@login_required
def get_transacoes():
    usuario_id = current_user.id  # Obter ID do usuário logado
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).all()
    return render_template('transacoes.html', transacoes=transacoes)


@app.route('/transacoes', methods=['GET', 'POST'])
@login_required
def transacoes():
    if request.method == 'POST':
        # Recebe dados do cliente
        data = request.json
        # Validação básica dos dados recebidos
        if not data or not all(k in data for k in ['descricao', 'valor', 'categoria', 'tipo', 'metodo_pagamento', 'data']):
            return jsonify({'success': False, 'message': 'Dados incompletos ou inválidos'}), 400

        try:
            # Criar nova transação
            nova_transacao = Transacao(
                descricao=data['descricao'],
                valor=float(data['valor']),
                categoria=data['categoria'],
                tipo=data['tipo'],
                metodo_pagamento=data['metodo_pagamento'],
                notas=data.get('notas', ''),  # Notas são opcionais
                usuario_id=current_user.id,  # ID do usuário logado
                data=datetime.strptime(data['data'], '%Y-%m-%d')  # Converte a data para um objeto datetime
            )
            db.session.add(nova_transacao)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Transação adicionada com sucesso!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao adicionar transação: {str(e)}'}), 500
           
    # Renderiza o template para requisições GET diretas (opcional)
    return render_template('transacoes.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/adicionar-conta', methods=['GET', 'POST'])
@login_required
def adicionar_conta():
    if request.method == 'POST':
        try:
            nome_banco = request.form['nome_banco']
            saldo_atual = float(request.form['saldo_atual'])
            tipo_conta = request.form['tipo_conta']

            # Ao criar uma nova conta, defina o saldo_atual para 0.0
            nova_conta = Contabancaria(
                nome_banco=nome_banco,
                saldo_atual=saldo_atual,  # Inicializando o saldo como 0.0
                tipo_conta=tipo_conta,
                usuario_id=current_user.id  # Associa a conta ao usuário logado
            )

            # Adicionando a conta ao banco de dados
            db.session.add(nova_conta)
            db.session.commit()

            # Flash de sucesso e redirecionamento
            flash('Conta adicionada com sucesso!', 'success')
            return redirect(url_for('tela_principal'))  # Redireciona para a tela principal

        except Exception as e:
            db.session.rollback()  # Desfaz a operação em caso de erro
            flash('Erro ao adicionar a conta. Tente novamente.', 'danger')
            return redirect(url_for('adicionar_conta'))  # Redireciona de volta para a página de adicionar conta

    # Renderiza o formulário para adicionar uma conta
    return render_template('adicionar_conta.html')




@app.route('/metas', methods=['GET', 'POST'])
@login_required
def metas():
    return render_template('metas.html')


from sqlalchemy import func


@app.route('/relatorio', methods=['GET'])
@login_required
def relatorio():
    usuario_id = current_user.id

    # Obter o resumo financeiro
    resumo = calcular_resumo_financeiro(usuario_id)

    if request.method == 'POST':
        # Recebe dados do cliente
        data = request.json
        # Validação básica dos dados recebidos
        if not data or not all(k in data for k in ['descricao', 'valor', 'categoria', 'tipo', 'metodo_pagamento', 'data']):
            return jsonify({'success': False, 'message': 'Dados incompletos ou inválidos'}), 400

        try:
            # Criar nova transação
            nova_transacao = Transacao(
                descricao=data['descricao'],
                valor=float(data['valor']),
                categoria=data['categoria'],
                tipo=data['tipo'],
                metodo_pagamento=data['metodo_pagamento'],
                notas=data.get('notas', ''),  # Notas são opcionais
                usuario_id=usuario_id,  # ID do usuário logado
                data=datetime.strptime(data['data'], '%Y-%m-%d')  # Converte a data para um objeto datetime
            )
            db.session.add(nova_transacao)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Transação adicionada com sucesso!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao adicionar transação: {str(e)}'}), 500

    # Para requisições GET, buscar transações do usuário logado
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).all()
    
    return render_template(
            'relatorio.html',
            totalReceitas=resumo['receita_total'],
            totalDespesas=resumo['despesa_total'],
            balanco=resumo['balanco'], transacoes=transacoes
        )



if __name__ == '__main__':
    app.run(debug=True)