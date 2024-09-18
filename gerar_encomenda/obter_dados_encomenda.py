'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox, Label, Entry, filedialog
from tabulate import tabulate

dados_encomenda = []

def buscar_dados_eship(usuario):
	# app = tk.Tk()
	# app.withdraw()  # Oculta a janela principal
	# file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
	# if not file_path:
	# 	messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
	# 	return
    
	# dados = pd.read_excel(file_path, engine='openpyxl')
	# dados_encomenda.clear()  # Limpa dados anteriores

	# messagebox.showinfo("Informação", "Arquivo importado com sucesso")
    
    # # Pergunta ao usuário se deseja continuar
	# resposta = messagebox.askquestion('''
	# 	"Confirmação", f'*** !!! ATENÇÂO !!! ***\n\n\n
	# 	Tem certeza que deseja realizar a Emissão em lote?\n
	# 	Essa ação será irrevercível.\n\n\n
	# 	{usuario}, você confirma a emissão?'
	# ''')
    
	# if resposta == 'no':
	# 	messagebox.showinfo("Informação", "Operação cancelada.")
	# 	return

	# for coluna_a, coluna_b, coluna_c in zip(dados.iloc[:, 0], dados.iloc[:, 1], dados.iloc[:, 2]):
	# 	print(f'Franquia: {coluna_a} | Cliente: {coluna_b} | Ordem: {coluna_c, type(coluna_c)}')
		url = 'https://amplo.eship.com.br/v3/?api=&funcao=webServiceGetOrdem'

		payload = {
			"ordem": '644936'
		}		
		apikey = load_apikey()

		# Cabeçalhos da requisição
		headers = {
			'Content-Type': 'application/json',
			'api': apikey
		}

		# Realiza a requisição GET
		response = requests.get(url, headers=headers, json=payload)
		response_data = response.json()
		
		ordem = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['idOrdem']
		print('='*60)
		print('ORDEM vinda da api................')
		print(ordem)

		remetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['remetente']
		cnpj_remetente = remetente['cnpj']
		razaoSocial = remetente['razaoSocial']
		print('='*60)
		print('REMETENTE................')
		print(cnpj_remetente)
		print(razaoSocial  )
	# 	enderecoRemetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoRemetente']
	
	# 	destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['destinatario']
	# 	print('DESTINATARIO')
	# 	print(destinatario)
	# 	print('='*60)

	# 	print('ENDEREÇO - DESTINATARIO')
	# 	enderecoDestinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoDestinatario']
	# 	print(enderecoDestinatario)
	# 	print('='*60)

	# 	print('TOMADOR')
	# 	tomador = 'HARD CODE'
	# 	print(tomador)
	# 	print('='*60)

	# 	print('USUARIO EMISSOR')
	# 	usuario_emissor = 'REVISAR'
	# 	print(usuario_emissor)
	# 	print('='*60)

	# 	print('PESO ')
	# 	peso = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['produto']
	# 	print(peso)
	# 	print('='*60)

	# 	dados_encomenda.append({
	# 	        'ORDEM': ordem,
	# 	        'remetente': remetente,
	# 	        'enderecoRemetente': enderecoRemetente,
	# 	        'destinatario': destinatario,
	# 	        'enderecoDestinatario': enderecoDestinatario,
	# 			'tomador': tomador,
	# 			'UsuarioLog': usuario
	# 	    })
		
	# df = pd.DataFrame(dados_encomenda)
	# print(df)

	# export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
	# if export_file_path:
	# 	df.to_excel(export_file_path, index=False)
	# 	messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")




	##################3 REVISAR DAQUI PARA BAIXO #############################################################

		
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

		

