import sys
import os
import requests
import json
# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authentication.authenticate import authenticate_sessao_embarcador, authenticate_sessao
from fiscal.obter_valor_frete import get_vtprest

# Autenticação
sessao = authenticate_sessao_embarcador()
def get_doc_fiscal(ordem):
    # URL da API
    url = "https://api.track3r.com.br/v2/api/ConsultaDocumentoFiscal"

    # Payload (dados para envio)
    payload = {     
                "sessao": sessao['sessao'],
                "encomendas": [
                    {
                    # "encomenda": encomenda,
                    # "numeroNota": "761822"  # não tem CTE emitido
                    # "numeroNota": "758048"  # tem CTE emitido
                    "numeroNota": ordem # tem CTE emitido
                    }
                ]
            }

    # Cabeçalhos da requisição
    headers = {
        'Content-Type': 'application/json'
    }

    # Envio da requisição
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
        data = response.json() 

        numeroCTe = data['encomendas'][0]['numeroCTe']

        if numeroCTe is None:
            mensagem = {'Encomenda': data['encomendas'][0]['encomenda'], 'msg': 'CTE não emitido'}
            print(mensagem)
            return numeroCTe, valor_prestacao_serviço, dacte
        
        url_xml = data['encomendas'][0]['caminhoXML']
        dacte = data['encomendas'][0]['caminhoDACTE']

        valor_prestacao_serviço = get_vtprest(url_xml)
        return numeroCTe, valor_prestacao_serviço, dacte
    
    except requests.exceptions.RequestException as e:
        mensagem =f"Erro na requisição: {e}"
        print(mensagem)
        return mensagem
    