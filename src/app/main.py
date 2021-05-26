# importando as bibliotecas
import os
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
# import pandas as pd
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

modelo = pickle.load(open('../../models/modelo.sav', 'rb'))
# modelo = pickle.load(open('modelo.sav', 'rb'))

# # lendo a base
# df = pd.read_csv('casas.csv')

# # filtrando as colunas
colunas = ['tamanho', 'ano', 'garagem']
# # colunas = ['tamanho', 'preco']
# # df = df[colunas]

# # separando em X e y
# X = df.drop('preco', axis=1)
# y = df['preco']

# # separando em treino e teste
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.3, random_state=42)

# # ajustando o modelo
# modelo = LinearRegression()
# modelo.fit(X_train, y_train)

# instanciando o pacote em uma variável
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
# app.config['BASIC_AUTH_USERNAME'] = 'caique'
# app.config['BASIC_AUTH_PASSWORD'] = 'senha'

basic_auth = BasicAuth(app)

# definindo uma rota da API e sua respectiva função
@app.route('/')
def home():
    return 'Minha primeira API.'

# criando uma rota para servir o modelo de sentimento
@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polarity = tb_en.sentiment.polarity
    return 'A polaridade desta frase é: {}'.format(polarity)

# criando uma rota para servir o modelo de preços
@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json() # vai trazer o json que o usuário enviar
    dados_input = [dados[col] for col in colunas] # garante que os dados estejam na ordem correta
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

# @app.route('/cotacao/<int:tamanho>')
# def cotacao(tamanho):
#     preco = modelo.predict([[tamanho]])
#     return str(preco)

# roda a aplicação
app.run(debug=True, host='0.0.0.0')