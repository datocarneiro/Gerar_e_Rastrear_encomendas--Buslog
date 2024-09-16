'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
import requests
import pandas as pd
import tkinter as tk


def dados_eship():
	apikey = load_apikey()

	url = 'https://amplo.eship.com.br/v3/?api=&funcao=webServiceGetOrdem'



	# Cabeçalhos da requisição
	headers = {
		'Content-Type': 'application/json',
		'api': apikey
	}

	# Dados da requisição
	payload = {
		"ordem": "644936",
	}

	# Realiza a requisição GET
	response = requests.get(url, headers=headers, json=payload)
	response_data = response.json()

	# Exibe a resposta
	print(response.status_code)

	destinatario = response_data['corpo']['body']['dados'][0]['destinatario']
	nome = destinatario["nome"]
	cpf = destinatario["cpf"]
	status = destinatario["status"]

	print(destinatario)
	print('='*50)
	print(nome)
	print(cpf)


