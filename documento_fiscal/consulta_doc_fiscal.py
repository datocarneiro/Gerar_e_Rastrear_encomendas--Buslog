import sys
import os
import requests
import json

# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authentication.authenticate import authenticate_sessao

# Autenticação
sessao = authenticate_sessao()

print(sessao)

# URL da API
url = "https://api.track3r.com.br/v2/api/ConsultaDocumentoFiscal"

# Payload (dados para envio)
payload = {
        "sessao": "e6ac81ba-5e82-476b-8b70-af7ac96258d9",
        "encomendas": [
            {
            "encomenda": "27207565",
            "numeroNota": "752418 "
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
    response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
    print(response.json())  # Exibe a resposta da API
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")