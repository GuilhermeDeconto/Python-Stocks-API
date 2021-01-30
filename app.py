from flask import Flask, request, jsonify
from yahooquery import Ticker
from datetime import datetime
from pandas import DataFrame
from operator import itemgetter
import js2py
import pytz
import random
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "API para gerar valores de ações"


@app.route('/acoes/<stock_symbol>', methods=['GET'])
def get_stock_info(stock_symbol):
    
    ticker_acao = Ticker(stock_symbol)
    resultado = ticker_acao.get_modules(['financialData','quoteType'])

    codigo = itemgetter(stock_symbol)(resultado)
    retorno = {'result': codigo}
    return json.dumps(retorno), 200


@app.route('/acoes/history/<stock_symbol>', methods=['GET'])
def get_stock_historical_data(stock_symbol):
    
    resultado = Ticker(stock_symbol, formatted=True, asynchronous=True).history(period='1y', interval='1d')
    df = resultado

    retorno = df.to_json(orient='table')

    data = json.loads(retorno)

    print({ 'result' : data['data'] })
    
    return json.dumps({ 'result' : data['data'] }), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
