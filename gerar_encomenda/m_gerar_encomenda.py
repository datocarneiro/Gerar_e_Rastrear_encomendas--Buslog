import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.authenticate import authenticate_sessao as aut, load_usuario_permitidos
from gerar_encomenda.obter_dados_encomenda import buscar_dados_eship
import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox, Label, Entry, filedialog
import json
from dotenv import load_dotenv


def enviarobjeto(chave_session, usuario):

	if usuario == "":
		messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
		return
	
	usuario_formatado = usuario.capitalize()
	usuarios_permitidos = load_usuario_permitidos()
	
	if usuario_formatado not in usuarios_permitidos:
		messagebox.showinfo("Informação",
            f'''    *** !!! ATENÇÂO !!! ***\n\n\n
            Usuário: "{usuario_formatado}" sem permissão ! ... \n\n
            Verifique o usuario registrado.\n
            Ou entre em contato com a equipe de TI
        ''')
		return

	
	app = tk.Tk()
	app.withdraw()  # Oculta a janela principal
	file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
	if not file_path:
		messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
		return
    
	messagebox.showinfo("Informação", "Arquivo importado com sucesso")

	# Pergunta ao usuário se deseja continuar
	resposta = messagebox.askquestion("Confirmação",
		f'''*** !!! ATENÇÂO !!! ***\n\n
		Tem certeza que deseja realizar a Emissão em lote?\n
		Essa ação será irrevercível.\n\n\n
		{usuario_formatado}, você confirma a emissão?''')
	
	if resposta == 'no':
		messagebox.showinfo("Informação", "Operação cancelada.")
		return
	
	dados = pd.read_excel(file_path, engine='openpyxl')

	dados_emitidos = []
	for  coluna_a, coluna_b, coluna_c in zip(dados.iloc[:, 0], dados.iloc[:, 1], dados.iloc[:, 2]):
		franquia = coluna_a
		ordem = coluna_c
		
		dados_para_envio = buscar_dados_eship(franquia, ordem, usuario_formatado)
		print(f'Dadous para envio retornado: \n {dados_para_envio}')

		print('='*90)
		dados_emitidos.append(*dados_para_envio)

	df = pd.DataFrame(dados_emitidos)
	print(df)
	export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
	if export_file_path:
		# df.to_json(export_file_path, index=False)
		df.to_excel(export_file_path, index=False)
			
	messagebox.showinfo("Informação", "Retornamos ao modulo gerar .....FIM")

	################################ AQUI COMEÇA O ENVIOU ############################

	# chave = chave_session['sessao']
	# url = "https://api.track3r.com.br/v2/api/GerarEncomendas"

	# payload = json.dumps(
	# 	{
	# 	"sessao": chave,
	# 	"id_servico": 1,    # 1=Entrega, 4=Reversa, 7=Entrega na Loja, 8=Lotação, 9=Retira
	# 	#   "numero_carga": "2",      
	# 	#                     
	# 	"encomendas": [

	# )
	# headers = {
	# 	'Content-Type': 'application/json'
	# }

	# response = requests.request("POST", url, headers=headers, data=payload)

	# print(f'fim do envio {response.text}')

	# return response

	return 


