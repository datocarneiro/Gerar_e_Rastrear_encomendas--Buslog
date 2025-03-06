import requests
import os
from dotenv import load_dotenv

def load_token():
    load_dotenv()
    token = os.getenv("TOKEN")
    return token

def load_token_cotacao():
    load_dotenv()
    token_cotacao = os.getenv("TOKEN_EMBARCADOR")
    return token_cotacao

def authenticate_sessao():
    try:
        token = load_token()
        url = f"http://api.track3r.com.br/v2/api/Autenticacao?token={token}"
        response = requests.get(url)
        retorno = response.json()
    except TimeoutError as e:
        print(f'erro: {e}')
        return e
    return retorno
    
def authenticate_sessao_embarcador():
    try:
        token_embarcador = load_token_cotacao()
        url = f"http://api.track3r.com.br/v2/api/Autenticacao?token={token_embarcador}"
        response = requests.get(url)
        retorno = response.json()
    except TimeoutError as e:
        print(f'erro: {e}')
        return e
    return retorno

def load_apikey():
    load_dotenv()
    apikey = os.getenv("APIKEY")
    return apikey

def load_usuario_permitidos():
    load_dotenv()
    usuario_permitidos = os.getenv("USUARIOS_PERMITIDOS")
    return usuario_permitidos

def registra_usuario(usuario):
    # Aqui você coloca a lógica de registro do usuário
    usuario_formatado = usuario.capitalize()
    print(f"Usuário registrado: {usuario_formatado}")
    
