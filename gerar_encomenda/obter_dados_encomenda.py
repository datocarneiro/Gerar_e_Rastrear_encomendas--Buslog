'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
from gerar_encomenda.dados_faturamento import dados_volumes
from tkinter import messagebox, filedialog
import requests
import re


def buscar_dados_eship(franquia, ordem, usuario):
	dados_encomenda = []	
	dados_encomenda.clear()  # Limpa dados anteriores
	
	apikey = load_apikey()

	url = 'https://amplo.eship.com.br/v3/?api=&funcao=webServiceGetOrdem'

	payload = {
		"ordem": ordem,			#para teste hard code '648986' # 649739 (F)    650224 (J) 648986 (luiz)
	}		

	# Cabeçalhos da requisição
	headers = {
		'Content-Type': 'application/json',
		'api': apikey
	}

	# Realiza a requisição GET
	response = requests.get(url, headers=headers, json=payload)
	response_data = response.json()

	
	# print('.........................................encomendas.......................................')
	'''
	###################### ... PARA "id_produto" ... ####################################

	SERVÇO ENTREGA
	"id_produto" = 1225 -> COLETA x ENTREGA
	"id_produto" = 1224 -> BALCÃO x ENTREGA

	SERVIÇO RETIRA
	"id_produto" = 1177 -> COLETA x BALCÃO
	"id_produto" = 1170 -> BALCÃO x BALCÃO

	'''
	id_produto = 1225 

	numero_pedido = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['idOrdem']
	# print(f'numero_pedido:', numero_pedido)


	# print('.................................... documento_transportado ..............................')
	tipo_documento_transportado = 3  # // 1 NF, 2 NFC,  3 = Declaração
	# print(f'tipo:', tipo_documento_transportado)
	# print(f'numero:', numero_pedido)

	dimenssao_volume = dados_volumes(apikey, ordem)
	qtd_volume = len(dimenssao_volume)
	valor_ordem= f"{response_data['corpo']['body']['dados'][0]['valorTotal']:.2f}"
	valor_documento = float(valor_ordem)
	# print(f'quantidade_volumes:', qtd_volume)
	# print(f'valor_documento:', valor_documento)


	# print('......................................... Verifica Tipo_fiscal ......................................')
	def formata_cnpj(cnpj):
		# Remove qualquer caractere que não seja número
		cnpj = re.sub(r'\D', '', cnpj)
		
		# Verifica se tem 14 dígitos
		if len(cnpj) == 14:
			return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
		else:
			raise ValueError(f"CNPJ inválido: {cnpj}. Deve conter 14 dígitos.")
		

	def formata_cpf(cpf):
		# Remove qualquer caractere que não seja número
		cpf = re.sub(r'\D', '', str(cpf))  # Converte para string antes de remover caracteres

		# Verifica se tem 11 dígitos
		if len(cpf) == 11:
			return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
		else:
			# linha = i + 2 if i is not None else "desconhecida"  # Garante que a linha seja mostrada corretamente

			erro_msg = (
				f"Ordem: {ordem}, com falha!\n\n"
				f"{usuario}, confira os dados.\n\n"
				"Verifique se o cadastro está como 'INDEFINIDO', ajuste e informe o CNPJ."
			)

			# Exibir a mensagem antes de levantar o erro
			print(erro_msg)  # Garante que a mensagem seja exibida no console também
			messagebox.showerror("Erro", erro_msg)  # Mensagem de erro antes de levantar a exceção
			
			raise ValueError(erro_msg)


	def tipo_de_cadastro(cadastro, tipo_fiscal):	
		if tipo_fiscal == 1:
			# Pessoa Jurídica (PJ)
			tipo_pessoa = 'J'
			cnpj_cpf_cadastro = cadastro['cnpj']
			ie_cadastro = cadastro['ie']
			nome_cadastro = cadastro['razaoSocial']
			
			# Formatar o CNPJ (pode estar formatado ou não)
			cnpj_cpf_cadastro = formata_cnpj(cnpj_cpf_cadastro)
		else:
			# Pessoa Física (PF)
			tipo_pessoa = 'F'
			cnpj_cpf_cadastro = cadastro['cpf']
			ie_cadastro = ''
			nome_cadastro = cadastro['nome']
			
			# Formatar o CPF (pode estar formatado ou não)
			cnpj_cpf_cadastro = formata_cpf(cnpj_cpf_cadastro)
		return tipo_pessoa, cnpj_cpf_cadastro, ie_cadastro, nome_cadastro
	
	# print('................ ......................... REMETENTE ...................................')

	remetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['remetente']
	tipo_fiscal = remetente['tipoFiscal']['id']
	
	tipo_pessoa_remetente, cnpj_cpf_remetente, ie_remetente, nome_remetente = tipo_de_cadastro(remetente, tipo_fiscal)

	enderecoRemetente = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoRemetente']
	cep_remetente = enderecoRemetente['codigoPostal']
	bairro_remetente = enderecoRemetente['bairro']
	rua_remetente = enderecoRemetente['logradouro']
	num_remetente = enderecoRemetente['numero']
	complemento_remetente = enderecoRemetente['complemento']
	cidade_remetente = enderecoRemetente['municipio']['descricao']
	estado_remetente = enderecoRemetente['municipio']['estado']['sigla']

	# print('......................................... tomador_embarcador .........................................')
	cnpj_tomador_embarcador = '08.806.647/0001-17'
	ie_tomador_embarcador = '9040355992'
	razaoSocial_tomador_embarcador = 'Amplo Logistica e Armazenagem Ltda'
	cep_tomador_embarcador = '83412-585'
	bairro_tomador_embarcador = 'Canguiri'
	rua_tomador_embarcador = 'Pedro Zanetti'
	num_tomador_embarcador = '230'
	complemento_tomador_embarcador = 'Barracão 2'
	cidade_tomador_embarcador = 'Colombo'
	estado_tomador_embarcador = 'PR'

	# print('......................................... destinatario ......................................')

	destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['destinatario']
	tipo_fiscal = destinatario['tipoFiscal']['id']
	tipo_pessoa, cnpj_cpf_destinatario, ie_destinatario, nome_destinatario = tipo_de_cadastro(destinatario, tipo_fiscal)

	endereçoDestinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoDestinatario']
	cep_destinatario = endereçoDestinatario['codigoPostal']
	# Remove qualquer caractere que não seja numérico
	cep_destinatario_numerico = re.sub(r'\D', '', cep_destinatario)
	# print(f'cep destinatario {cep_destinatario},  {type(cep_destinatario)}')
	# print(f'cep destinatario {cep_destinatario_numerico},  {type(cep_destinatario_numerico)}')
	bairro_destinatario = endereçoDestinatario['bairro']
	rua_destinatario = endereçoDestinatario['logradouro']
	num_destinatario = endereçoDestinatario['numero']
	complemento_destinatario = endereçoDestinatario['complemento']
	cidade_destinatario = endereçoDestinatario['municipio']['descricao']
	estado_destinatario = endereçoDestinatario['municipio']['estado']['sigla']


	# print('....................................... Usauario emmissao ...............')
	# print('REVISAR >>>>>')
	# print('.......................................... volumes...............')
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
			"peso_cubado": round(float((volume['alturaVolume'])/1000 * (volume['larguraVolume']/1000 ) * (volume['comprimentoVolume']/1000) * 200), 2)


		})
	volumes = lista_volumes
	# print(volumes)

	dados_encomenda.append({
		# 'franquia': franquia,
		"id_produto": id_produto,
		"numero_pedido": numero_pedido,
		"documento_transportado":{
			"tipo": tipo_documento_transportado,
			"numero": numero_pedido,
			"quantidade_volumes": qtd_volume,
			"valor_documento": valor_documento
		},
		"embarcador":{
			"cnpj": cnpj_tomador_embarcador,
			"razao_social": razaoSocial_tomador_embarcador,
			"nome_fantasia": f'{razaoSocial_tomador_embarcador} ({usuario})',
			"endereco":{
				"cep": cep_tomador_embarcador,
				"bairro": bairro_tomador_embarcador,
				"rua": rua_tomador_embarcador,
				"numero": num_tomador_embarcador,
				"complemento": complemento_tomador_embarcador,
				"cidade": cidade_tomador_embarcador,
				"estado": estado_tomador_embarcador
			}
		},
		"tomador":{
			"cnpj": cnpj_tomador_embarcador,
			"inscricao_estadual": ie_tomador_embarcador,
			"razao_social": razaoSocial_tomador_embarcador,
			"endereco": {
				"cep": cep_tomador_embarcador,
				"bairro": bairro_tomador_embarcador,
				"rua": rua_tomador_embarcador,
				"numero": num_tomador_embarcador,
				"complemento": complemento_tomador_embarcador,
				"cidade": cidade_tomador_embarcador,
				"estado": estado_tomador_embarcador
			}
		},
		"loja_remetente": {
			"cnpj_cpf": cnpj_cpf_remetente,
			"inscricao_estadual": ie_remetente,
			"tipo_pessoa": tipo_pessoa_remetente,
			"nome": nome_remetente,
			"endereco": {
			"cep": cep_remetente,
			"bairro": bairro_remetente,
			"rua": rua_remetente,
			"numero": num_remetente,
			"complemento": complemento_remetente,
			"cidade": cidade_remetente,
			"estado": estado_remetente
			}
		},
		"destinatario":{
			"tipo_pessoa": tipo_pessoa,
			"cnpj_cpf": cnpj_cpf_destinatario,
			"inscricao_estadual": ie_destinatario,
			"nome": nome_destinatario,
			"endereco":{
				"cep": cep_destinatario_numerico,
				"bairro": bairro_destinatario,
				"rua": rua_destinatario,
				"numero": num_destinatario,
				"complemento": complemento_destinatario,
				"cidade": cidade_destinatario,
				"estado": estado_destinatario
			}
		},
		# "loja_remetente":{
		# 	# "cnpj_cpf": "478.517.310-62",
        # 	# "inscricao_estadual": "",
		# 	"tipo_pessoa": "F",
		# 	"nome": usuario
		# },
		"volumes": volumes
	})

	return dados_encomenda
