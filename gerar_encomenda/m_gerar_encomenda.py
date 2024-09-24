from inserir_tracking_pedido.inserir_tracking import inserir_trancking
from gerar_encomenda.obter_dados_encomenda import buscar_dados_eship
from authentication.authenticate import load_usuario_permitidos
from tkinter import messagebox, filedialog
import tkinter as tk
import pandas as pd
import requests
import json

def gerar_encomenda(chave_session, usuario, progress):
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

	resposta = messagebox.askquestion("Confirmação",
		f'''*** !!! ATENÇÂO !!! ***\n\n
		Deseja realizar a emissão em lote?\n
		Essa ação será irrevercível.\n\n\n
		{usuario_formatado}, você confirma a emissão?''')
	
	if resposta == 'no':
		messagebox.showinfo("Informação", "Operação cancelada.")
		return
	try: 
		dados = pd.read_excel(file_path, engine='openpyxl')

		total_rows = len(dados)
		progress['maximum'] = total_rows  # Define o valor máximo da barra de progresso

		dados_emitidos = []
		for i, (coluna_a, coluna_b, coluna_c) in enumerate(zip(dados.iloc[:, 0], dados.iloc[:, 1], dados.iloc[:, 2])):
			franquia = coluna_a
			ordem = coluna_c
			
			dados_para_envio = buscar_dados_eship(franquia, ordem, usuario_formatado)
			print(f'Dadous para envio retornado: \n {dados_para_envio}')

			print('='*90)
			dados_emitidos.append(*dados_para_envio)

			# Atualiza a barra de progresso
			progress['value'] = i + 1  # Atualiza o progresso
			app.update_idletasks()  # Atualiza a interface gráfica
	
	except KeyError as e:
		messagebox.showinfo("Informação", 
			f'''Erro: \n
            Base do arquivo é inválida\n
            {usuario_formatado}, confira o arquivo importado.''')
		return

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
		resposta_buslog = {
							"totalProcessado": 1,
							"totalRecebidoSucesso": 1,
							"totalRecebidoErro": 0,
							"status": [
								{
								"status": 'true',
								"descricao": "Nota Recebida",
								"notaFiscal": "644936",
								"protocolo": "39696503",
								"encomenda": "25258433",
								"volumes": [
									{
									"volume": 1,
									"codigoVolume": "44982667"
									}
								]
								}
							]
							}
		cod_encomenda = int(resposta_buslog['status'][0]['encomenda'])
		inserir_trancking(cod_encomenda, ordem)
		dados_emitidos.append({'tracking': cod_encomenda})

	df = pd.DataFrame(dados_emitidos, )
	print(df)
	export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
	if export_file_path:
		# df.to_json(export_file_path, index=False)
		df.to_excel(export_file_path, index=False)
			
	messagebox.showinfo("Informação", "Retornamos ao modulo gerar .....FIM")
	
	return 


