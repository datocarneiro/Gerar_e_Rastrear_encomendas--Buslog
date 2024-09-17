'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
import requests
import pandas as pd
import tkinter as tk
from tabulate import tabulate

def dados_eship():
	dados_encomenda = []
	apikey = load_apikey()

	url = 'https://amplo.eship.com.br/v3/?api=&funcao=webServiceGetOrdem'
	# url = 'http://amplo.eship.com.br/v2/?funcao=webServiceConsultarDadosVolumesFaturamento'

	# Cabeçalhos da requisição
	headers = {
		'Content-Type': 'application/json',
		'api': apikey
	}

	# Dados da requisição
	payload = {
		"ordem": "00635445"
	}

	# Realiza a requisição GET
	response = requests.get(url, headers=headers, json=payload)
	response_data = response.json()
	
	ordem = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['idOrdem']
	print('='*60)
	print('ORDEM')
	print(ordem)
	print('='*60)

	remetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['remetente']
	print('REMETENTE')
	print(remetente)
	print('='*60)

	enderecoRemetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoRemetente']
	print('ENDEREÇO - REMETENTE')
	print(enderecoRemetente)
	print('='*60)

	destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['destinatario']
	print('DESTINATARIO')
	print(destinatario)
	print('='*60)
	print('ENDEREÇO - DESTINATARIO')
	enderecoDestinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoDestinatario']
	print(enderecoDestinatario)
	print('='*60)

	print('TOMADOR')
	tomador = 'REVISAR'
	print(tomador)
	print('='*60)

	print('USUARIO EMISSOR')
	usuario_emissor = 'REVISAR'
	print(usuario_emissor)
	print('='*60)

	print('PESO ')
	peso = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['produto']
	print(peso)
	print('='*60)


	# dados_encomenda.append({
    #         'ORDEM': "|000000",
    #         'ENCOMENDA': "|1111111",
    #         'NOME': f'|{nome}',
    #         'CPF|CNPJ': f'{cnpj}',
    #         'IE': f'{ie}',
    #         'RG': f'{rg}'
    #     })
	# df = pd.DataFrame(dados_encomenda)
	# print(tabulate(df, headers='keys', tablefmt='grid'))
	return

	# "tipo": null,
	# "descricao": "Física",
	# "somenteleitura": true
	# },
	# "classificacao": null,
	# "status": {
	# "id": 1,
	# "descricao": "Ativado",
	# "cor": {
	# "id": 3,
	# "descricao": "VERDE",
	# "hexadecimal": "#00e676",
	# "corContraste": 6
	# },
	# "idCor": null,
	# "svg": null
	# },
	# "cadastroSuperior": null,
	# "idCadastroSuperior": 2,
	# "enderecos": [],
	# "enderecoPrincipal": null,
	# "contatos": [],
	# "codigo": "DatoAmplo",
	# "configuracaoCadastro": null,
	# "info": null



