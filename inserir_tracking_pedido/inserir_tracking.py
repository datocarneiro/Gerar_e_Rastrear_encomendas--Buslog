from authentication.authenticate import load_apikey
import tkinter as tk
from tkinter import messagebox, Label, ttk
import requests
import json


def inserir_trancking(tracking, ordem):
    apikey = load_apikey()
    url = "https://amplo.eship.com.br/v2/?funcao=webServiceInserirRastreamento"

    payload = json.dumps({
    "numeroOrdem": ordem,
    "rastreamentos": [
        {
        "codigoRastreio": tracking
        }
    ]
    })
    headers = {
    'Api': apikey,
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return

    