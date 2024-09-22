from authentication.authenticate import load_apikey
from tkinter import messagebox
import requests
import json


def inserir_trancking(ordem, tracking):
    # apikey = load_apikey()
    # url = "https://amplo.eship.com.br/v2/?funcao=webServiceInserirRastreamento"

    # payload = json.dumps({
    # "numeroOrdem": ordem,
    # "rastreamentos": [
    #     {
    #     "codigoRastreio": tracking
    #     }
    # ]
    # })
    # headers = {
    # 'Api': apikey,
    # 'Content-Type': 'application/json',
    # }

    # response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    messagebox.showinfo("Informação", f'Aqui gravamos o tracking "{tracking}"no pedido')
