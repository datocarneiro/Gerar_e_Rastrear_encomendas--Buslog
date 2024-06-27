import requests
import os
from dotenv import load_dotenv

def load_token():
    # Carrega o token do arquivo .env
    load_dotenv()
    token = os.getenv("TOKEN")
    return token

def autenthicate_sessao():
    token = load_token()
    url = f"http://api.track3r.com.br/v2/api/Autenticacao?token={token}"
    response = requests.get(url)
    retorno = response.json()
    return retorno 

