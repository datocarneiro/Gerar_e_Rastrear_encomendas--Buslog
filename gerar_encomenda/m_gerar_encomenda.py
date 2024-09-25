from inserir_tracking_pedido.inserir_tracking import inserir_trancking
from gerar_encomenda.obter_dados_encomenda import buscar_dados_eship
from authentication.authenticate import load_usuario_permitidos
from tkinter import messagebox, filedialog
import tkinter as tk
import pandas as pd
import sqlite3
import requests
import json

def gerar_encomenda(chave_session, usuario, progress):
	if usuario == "":
		messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
		return
	
	usuario_formatado = usuario.capitalize()
	usuarios_permitidos = load_usuario_permitidos()
	
	if usuario_formatado not in usuarios_permitidos:
		messagebox.showinfo("Informação", f'''    *** !!! ATENÇÂO !!! ***\n\n\nUsuário: "{usuario_formatado}" sem permissão ! ...\n\nVerifique o usuario registrado.''')
		return

	app = tk.Tk()
	app.withdraw()  # Oculta a janela principal
	file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
	if not file_path:
		messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
		return
    
	messagebox.showinfo("Informação", "Arquivo importado com sucesso")

	resposta = messagebox.askquestion("Confirmação", f'''*** !!! ATENÇÂO !!! ***\n\nDeseja realizar a emissão em lote? Essa ação será irrevercível.\n\n\n{usuario_formatado}, você confirma a emissão?''')
	
	if resposta == 'no':
		messagebox.showinfo("Informação", "Operação cancelada.")
		return
	try: 
		dados = pd.read_excel(file_path, engine='openpyxl')

		total_rows = len(dados)
		progress['maximum'] = total_rows  # Define o valor máximo da barra de progresso

		dados_emitidos = []
		for i, (coluna_a, coluna_b, coluna_c) in enumerate(zip(dados.iloc[:, 0], dados.iloc[:, 1], dados.iloc[:, 2])):
			ordem = coluna_c
			franquia = coluna_a
			print(f'......................................................Progresso: {i+1}/{total_rows} - Ordem: {ordem}..............................................')
			
			dados_para_envio = buscar_dados_eship(franquia, ordem, usuario_formatado)

			print(f'Dados para envios : \n{dados_para_envio}')

			# Atualiza a barra de progresso
			progress['value'] = i + 1  # Atualiza o progresso
			app.update_idletasks()  # Atualiza a interface gráfica

			############################### AQUI COMEÇA O ENVIOU ############################

			chave = chave_session['sessao']
			url = "https://api.track3r.com.br/v2/api/GerarEncomendas"

			try: 
				payload = json.dumps(
					{
						"sessao": chave,
						"id_servico": 1,    # 1 = Entrega, 9 = Retira (se alterado verificar o valor para "id_produto" que deve ser passado no modulo gera_encomenda, ou na imagem na pasta "bases")
						#   "numero_carga": "2",      
						#                     
						"encomendas": dados_para_envio
					}
				)
				headers = {
					'Content-Type': 'application/json'
				}

				response = requests.request("POST", url, headers=headers, data=payload)

				response_data = response.json()
				print(response_data)

				print(f'fim do envio {response.text}')

				resposta_status = response_data['status']

				# Verifica se a chave 'status' está presente e contém dados
				if 'status' in response_data and resposta_status:
					encomenda = resposta_status[0].get('encomenda', '')
					
					# Verifica se o valor de 'encomenda' não está vazio ou inválido antes de converter
					if encomenda:
						try:
							cod_encomenda = int(encomenda)
							inserir_trancking(cod_encomenda, ordem)
						except ValueError:
							cod_encomenda = resposta_status[0]['descricao']
							raise ValueError(resposta_status[0]['descricao'])
					else:
						cod_encomenda = resposta_status[0]['descricao']
						raise ValueError(resposta_status[0]['descricao'])
				else:
					# Captura a mensagem de erro no response, caso exista
					error_message = response_data.get('mensagem', 'Erro desconhecido no servidor')
					cod_encomenda = error_message
					raise KeyError(f"Erro ao processar encomenda: {error_message}")

			except KeyError as e:
				print(f'Erro ao processar a encomenda: {e}')
				messagebox.showinfo("Informação", 
					f'''\nOrdem: {ordem} com falha!\n\nErro: {e}\n\n\n{usuario_formatado}, confira os dados.''')
				

			except ValueError as e:
				print(f'Erro de valor: {e}')
				messagebox.showinfo("Informação", 
					f'''\nOrdem: {ordem} com falha!\n\nErro de valor: {e}\n\n\n{usuario_formatado}, confira os dados.''')
				

			except Exception as e:
				print(f'Erro inesperado: {e}')
				messagebox.showinfo("Informação", 
					f'''\nOrdem: {ordem} com falha!\n\nErro inesperado: {e}\n\n\n{usuario_formatado}, confira os dados.''')
				
				

				


			# resposta_buslog = {
			# 					"totalProcessado": 1,
			# 					"totalRecebidoSucesso": 1,
			# 					"totalRecebidoErro": 0,
			# 					"status": [
			# 						{
			# 							"status": 'true',
			# 							"descricao": "Nota Recebida",
			# 							"notaFiscal": "644936",
			# 							"protocolo": "39696503",
			# 							"encomenda": "25258433",
			# 							"volumes": [
			# 								{
			# 								"volume": 1,
			# 								"codigoVolume": "44982667"
			# 								}
			# 							]
			# 						}
			# 					]
			# 				}
			
			

			# Criar o dicionário de encomenda com o código de rastreamento
			encomenda = {'tracking': cod_encomenda, 'LogUsuario': usuario_formatado}
			# Aqui, simplesmente use 'dados_para_envio' diretamente, sem o operador '*'
			desenpacotado = dados_para_envio

			# Loop para unir os dicionários
			for i in desenpacotado:
				# Combina o dicionário desenpacotado com o dicionário de encomenda
				unindo_dict = {**i, **encomenda}
				
				# Adiciona o dicionário combinado à lista 'dados_emitidos'
				dados_emitidos.append(unindo_dict)

	
	except KeyError as e:
		messagebox.showinfo("Informação", 
			f'''Erro: \n
            Base do arquivo é inválida\n
            {usuario_formatado}, confira o arquivo importado.''')
		return
	

	# Expandindo volumes em um DataFrame separado
	df = pd.json_normalize(dados_emitidos, record_path='volumes', 
								meta=[
									'id_produto', 
									'numero_pedido', 
									['documento_transportado', 'tipo'], 
									['documento_transportado', 'numero'], 
									['documento_transportado', 'quantidade_volumes'], 
									['documento_transportado', 'valor_documento'], 
									# ['embarcador', 'cnpj'], 
									# ['embarcador', 'razao_social'], 
									# ['embarcador', 'endereco', 'cep'], 
									# ['embarcador', 'endereco', 'bairro'], 
									# ['embarcador', 'endereco', 'rua'], 
									# ['embarcador', 'endereco', 'numero'], 
									# ['embarcador', 'endereco', 'complemento'], 
									# ['embarcador', 'endereco', 'cidade'], 
									# ['embarcador', 'endereco', 'estado'], 
									['tomador', 'cnpj'], 
									# ['tomador', 'inscricao_estadual'], 
									['tomador', 'razao_social'], 
									# ['tomador', 'endereco', 'cep'], 
									# ['tomador', 'endereco', 'bairro'], 
									# ['tomador', 'endereco', 'rua'], 
									# ['tomador', 'endereco', 'numero'], 
									# ['tomador', 'endereco', 'complemento'], 
									# ['tomador', 'endereco', 'cidade'], 
									# ['tomador', 'endereco', 'estado'], 
									# ['destinatario', 'tipo_pessoa'], 
									['destinatario', 'cnpj_cpf'], 
									['destinatario', 'inscricao_estadual'], 
									['destinatario', 'nome'], 
									['destinatario', 'endereco', 'cep'], 
									['destinatario', 'endereco', 'bairro'], 
									['destinatario', 'endereco', 'rua'], 
									['destinatario', 'endereco', 'numero'], 
									['destinatario', 'endereco', 'complemento'], 
									['destinatario', 'endereco', 'cidade'], 
									['destinatario', 'endereco', 'estado'], 
									# ['loja_remetente', 'tipo_pessoa'], 
									# ['loja_remetente', 'nome'], 
									'tracking'
								])
	
	# Conexão com o banco de dados SQLite (cria o arquivo se não existir)
	conn = sqlite3.connect('banco_de_dados/banco_de_dados_emissao.sqlite')
	# Salvar o DataFrame em uma tabela chamada 'encomendas'
	df.to_sql('encomendas', conn, if_exists='replace', index=False)
	# Fechar a conexão
	conn.close()

	# Exibir o DataFrame de volumes
	print("\nDataFrame com volumes:\n ")
	print(df)

	export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
	if export_file_path:
		# df.to_json(export_file_path, index=False)
		df.to_excel(export_file_path, index=False)
			
	messagebox.showinfo("Informação", "Retornamos ao modulo gerar .....FIM")
	
	return 


