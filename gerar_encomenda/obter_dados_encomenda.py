'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
from gerar_encomenda.dados_faturamento import dados_volumes
import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox, Label, Entry, filedialog
from tabulate import tabulate
import re

dados_encomenda = []

def buscar_dados_eship(usuario):
	global dados_encomenda
	app = tk.Tk()
	app.withdraw()  # Oculta a janela principal
	file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
	if not file_path:
		messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
		return
    
	dados = pd.read_excel(file_path, engine='openpyxl')
	dados_encomenda.clear()  # Limpa dados anteriores

	messagebox.showinfo("Informação", "Arquivo importado com sucesso")
    
    # Pergunta ao usuário se deseja continuar
	resposta = messagebox.askquestion('''
		"Confirmação", f'*** !!! ATENÇÂO !!! ***\n\n\n
		Tem certeza que deseja realizar a Emissão em lote?\n
		Essa ação será irrevercível.\n\n\n
		{usuario}, você confirma a emissão?'
	''')
    
	if resposta == 'no':
		messagebox.showinfo("Informação", "Operação cancelada.")
		return

	dados_encomenda.clear()  # Limpa dados anteriores

	for coluna_a, coluna_b, coluna_c in zip(dados.iloc[:, 0], dados.iloc[:, 1], dados.iloc[:, 2]):
		print(f'Franquia: {coluna_a} | Cliente: {coluna_b} | Ordem: {coluna_c, type(coluna_c)}')
		# ordem = '648986' # 649739 (F)    650224 (J) 648986 (luiz)
		ordem = coluna_c
		apikey = load_apikey()

		url = 'https://amplo.eship.com.br/v3/?api=&funcao=webServiceGetOrdem'

		payload = {
			"ordem": ordem,
		}		

		# Cabeçalhos da requisição
		headers = {
			'Content-Type': 'application/json',
			'api': apikey
		}

		# Realiza a requisição GET
		response = requests.get(url, headers=headers, json=payload)
		response_data = response.json()

		
		print('.........................................encomendas.......................................')
		id_produto = 1
		print('id_produto:', id_produto)

		numero_pedido = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['idOrdem']
		print(f'numero_pedido:', numero_pedido)


		print('.................................... documento_transportado ..............................')
		tipo_documento_transportado = 3  # // 1 NF, 2 NFC,  3 = Declaração
		print(f'tipo:', tipo_documento_transportado)
		print(f'numero:', numero_pedido)

		dimenssao_volume = dados_volumes(apikey, ordem)
		qtd_volume = len(dimenssao_volume)
		valor_documento = 'R$ 0,00'
		print(f'quantidade_volumes:', qtd_volume)
		print(f'valor_documento:', valor_documento)

		print('................ .........................embarcador ...................................')
		embarcador = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['remetente']
		cnpj_embarcador = embarcador['cnpj']
		razaoSocial_embarcador = embarcador['razaoSocial']
		print(f'cnpj_embarcador: ',cnpj_embarcador)
		print(f'razaoSocial_embarcador: ',razaoSocial_embarcador)
		endereçoEmbarcador = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoRemetente']
		cep_embarcador = endereçoEmbarcador['codigoPostal']
		bairro_embarcador = endereçoEmbarcador['bairro']
		rua_embarcador = endereçoEmbarcador['logradouro']
		num_embarcador = endereçoEmbarcador['numero']
		complemento_embarcador = endereçoEmbarcador['complemento']
		cidade_embarcador = endereçoEmbarcador['municipio']['descricao']
		estado_embarcador = endereçoEmbarcador['municipio']['estado']['sigla']
		print(f'cep_embarcador:', cep_embarcador)
		print(f'bairro_embarcador:', bairro_embarcador)
		print(f'rua_embarcador:', rua_embarcador)
		print(f'num_embarcador:', num_embarcador)
		print(f'complemento_embarcador:', complemento_embarcador)
		print(f'cidade_embarcador:', cidade_embarcador)
		print(f'estado_embarcador:', estado_embarcador)

		print('......................................... tomador .........................................')
		cnpj_tomador = '08.806.647/0001-17'
		ie_tomador = '9040355992'
		razaoSocial_tomador = 'Amplo Logistica e Armazenagem Ltda'
		cep_tomador = '83412-585'
		bairro_tomador = 'Canguiri'
		rua_tomador = 'Pedro Zanetti'
		num_tomador = '230'
		complemento_tomador = 'Barracão 2'
		cidade_tomador = 'Colombo'
		estado_tomador = 'PR'
		print('cnpj_tomador:', cnpj_tomador)
		print('ie_tomador:', ie_tomador)
		print('razaoSocial_tomador: ', razaoSocial_tomador)
		print('cep_tomador:', cep_tomador)
		print('bairro_tomador:', bairro_tomador)
		print('rua_tomador:', rua_tomador)
		print('num_tomador:', num_tomador)
		print('complemento_tomador:', complemento_tomador)
		print('cidade_tomador:', cidade_tomador)
		print('estado_tomador:', estado_tomador)
	
		print('......................................... destinatario ......................................')
		def formata_cnpj(cnpj):
			"""
			Formata um CNPJ que pode vir com 14 dígitos não formatados ou já formatado.
			"""
			# Remove qualquer caractere que não seja número
			cnpj = re.sub(r'\D', '', cnpj)
			
			# Verifica se tem 14 dígitos
			if len(cnpj) == 14:
				return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
			else:
				raise ValueError(f"CNPJ inválido: {cnpj}. Deve conter 14 dígitos.")

		def formata_cpf(cpf):
			# Remove qualquer caractere que não seja número
			cpf = re.sub(r'\D', '', cpf)
			# Verifica se tem 11 dígitos
			if len(cpf) == 11:
				return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
			else:
				raise ValueError(f"CPF inválido: {cpf}. Deve conter 11 dígitos.")

		def tipo_de_destinatario(destinatario, tipo_fiscal):	
			if tipo_fiscal == 1:
				# Pessoa Jurídica (PJ)
				tipo_pessoa = 'J'
				cnpj_cpf_destinatario = destinatario['cnpj']
				ie_destinatario = destinatario['ie']
				nome_destinatario = destinatario['razaoSocial']
				
				# Formatar o CNPJ (pode estar formatado ou não)
				cnpj_cpf_destinatario = formata_cnpj(cnpj_cpf_destinatario)
			
			else:
				# Pessoa Física (PF)
				tipo_pessoa = 'F'
				cnpj_cpf_destinatario = destinatario['cpf']
				ie_destinatario = ''
				nome_destinatario = destinatario['nome']
				
				# Formatar o CPF (pode estar formatado ou não)
				cnpj_cpf_destinatario = formata_cpf(cnpj_cpf_destinatario)
			
			return tipo_pessoa, cnpj_cpf_destinatario, ie_destinatario, nome_destinatario

		# Exemplo de uso
		destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['destinatario']
		tipo_fiscal = destinatario['tipoFiscal']['id']
		tipo_pessoa, cnpj_cpf_destinatario, ie_destinatario, nome_destinatario = tipo_de_destinatario(destinatario, tipo_fiscal)

		endereçoDestinatario = destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoDestinatario']
		cep_destinatario = destinatario['codigoPostal']
		bairro_destinatario = destinatario['bairro']
		rua_destinatario = destinatario['logradouro']
		num_destinatario = destinatario['numero']
		complemento_destinatario = destinatario['complemento']
		cidade_destinatario = destinatario['municipio']['descricao']
		estado_destinatario = destinatario['municipio']['estado']['sigla']
		print(f'tipo_pessoa:', tipo_pessoa)
		print(f'cnpj_cpf_destinatario:', cnpj_cpf_destinatario)
		print(f'ie_destinatario:', ie_destinatario)
		print(f'nome_destinatario:', nome_destinatario)

		print(f'cep_destinatario:', cep_destinatario)
		print(f'bairro_destinatario:', bairro_destinatario)
		print(f'rua_destinatario:', rua_destinatario)
		print(f'num_destinatario:', num_destinatario)
		print(f'complemento_destinatario:', complemento_destinatario)
		print(f'cidade_destinatario:', cidade_destinatario)
		print(f'estado_destinatario:', estado_destinatario)
	


		print('....................................... Usauario emmissao ...............')
		print('REVISAR >>>>>')

		print('.......................................... volumes...............')
		# print(dimenssao_volume)
		lista_volumes = []
		volumes_ordem = dimenssao_volume
		for volume in volumes_ordem:
			lista_volumes.append({
				"codigo_etiqueta": volume['codigoVolume'],
				"altura": float(volume['alturaVolume']/1000),
				"largura": float(volume['larguraVolume']/1000),
				"comprimento": float(volume['comprimentoVolume']/1000),
				"peso_real": float(volume['pesoVolume']/1000),
				"peso_cubado": float((volume['alturaVolume'])/1000 * (volume['larguraVolume']/1000 ) * (volume['comprimentoVolume']/1000) * 200)


			})
		volumes = lista_volumes
		print(volumes)

		dados_encomenda.append({
			'id_produto': id_produto,
			'numero_pedido': numero_pedido,
			'tipo': tipo_documento_transportado,
			'numero': numero_pedido,
			'quantidade_volumes': qtd_volume,
			'valor_documento': valor_documento
		})

	print('=' * 80)
	print(f'\nDADOS ENCOMENDA ANTES DO DATAFRAME::::::::')	

	
	print('=' * 80)
	df = pd.DataFrame(dados_encomenda)
	print(f'DATAFRAME::::::::\n{df}')

	export_file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos", "*.json")])
	if export_file_path:
		df.to_json(export_file_path, index=False)
		# df.to_excel(export_file_path, index=False)
		messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")
