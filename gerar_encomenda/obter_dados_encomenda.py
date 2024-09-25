'''Iniciando modulo para buscar dados de encomenda'''
from authentication.authenticate import load_apikey
from gerar_encomenda.dados_faturamento import dados_volumes
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

	# print('................ .........................embarcador ...................................')
	embarcador = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['remetente']
	cnpj_embarcador = embarcador['cnpj']
	razaoSocial_embarcador = embarcador['razaoSocial']
	endereçoEmbarcador = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoRemetente']
	cep_embarcador = endereçoEmbarcador['codigoPostal']
	bairro_embarcador = endereçoEmbarcador['bairro']
	rua_embarcador = endereçoEmbarcador['logradouro']
	num_embarcador = endereçoEmbarcador['numero']
	complemento_embarcador = endereçoEmbarcador['complemento']
	cidade_embarcador = endereçoEmbarcador['municipio']['descricao']
	estado_embarcador = endereçoEmbarcador['municipio']['estado']['sigla']

	# print('......................................... tomador .........................................')
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

	# print('......................................... destinatario ......................................')
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

	destinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['destinatario']
	tipo_fiscal = destinatario['tipoFiscal']['id']
	tipo_pessoa, cnpj_cpf_destinatario, ie_destinatario, nome_destinatario = tipo_de_destinatario(destinatario, tipo_fiscal)

	endereçoDestinatario = response_data['corpo']['body']['dados'][0]['produtosOrdem'][0]['ordem']['enderecoDestinatario']
	cep_destinatario = endereçoDestinatario['codigoPostal']
	# Remove qualquer caractere que não seja numérico
	cep_destinatario_numerico = re.sub(r'\D', '', cep_destinatario)
	print(f'cep destinatario {cep_destinatario},  {type(cep_destinatario)}')
	print(f'cep destinatario {cep_destinatario_numerico},  {type(cep_destinatario_numerico)}')
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
			"cnpj": cnpj_embarcador,
			"razao_social": f'{razaoSocial_embarcador} ({usuario})',
			"nome_fantasia": f'{razaoSocial_embarcador} ({usuario})',
			"endereco":{
				"cep": cep_embarcador,
				"bairro": bairro_embarcador,
				"rua": rua_embarcador,
				"numero": num_embarcador,
				"complemento": complemento_embarcador,
				"cidade": cidade_embarcador,
				"estado": estado_embarcador
			}
		},
		"tomador":{
			"cnpj": cnpj_tomador,
			"inscricao_estadual": ie_tomador,
			"razao_social": razaoSocial_tomador,
			"endereco": {
				"cep": cep_tomador,
				"bairro": bairro_tomador,
				"rua": rua_tomador,
				"numero": num_tomador,
				"complemento": complemento_tomador,
				"cidade": cidade_tomador,
				"estado": estado_tomador
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
