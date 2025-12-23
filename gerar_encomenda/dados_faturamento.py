import requests
import json

def dados_volumes(apikey, ordem):

	print('vai entrar na Api de volumes ')
	url = "https://amplo.eship.com.br/v2/?funcao=webServiceConsultarDadosVolumesFaturamento"

	payload = json.dumps({
	"numeroOrdem": ordem
	})
	headers = {
	'Content-Type': 'application/json',
	'api': apikey
	}

	

	response = requests.request("POST", url, headers=headers, data=payload)
	response_data = response.json()
	# print('vai sair na Api de volumes ')
	# print(f'response volumes :::::: {response_data} ')

	dadosFaturamento = response_data['corpo']['classePadrao']['dadosFaturamento'][0]['dados']

	dados_volumes = dadosFaturamento

	print('retornando da função de volumes ')

	return dados_volumes




