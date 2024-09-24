import requests
import json

def dados_volumes(apikey, ordem):
	url = "http://amplo.eship.com.br/v2/?funcao=webServiceConsultarDadosVolumesFaturamento"

	payload = json.dumps({
	"numeroOrdem": ordem
	})
	headers = {
	'Content-Type': 'application/json',
	'api': apikey
	}

	response = requests.request("GET", url, headers=headers, data=payload)
	response_data = response.json()

	dadosFaturamento = response_data['corpo']['classePadrao']['dadosFaturamento'][0]['dados']

	dados_volumes = dadosFaturamento

	return dados_volumes




