import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import json


def enviarobjeto(chave):
  # chave = chave_session['sessao']
  url = "https://api.track3r.com.br/v2/api/GerarEncomendas"

  payload = json.dumps(
    {
    "sessao": 'cdfc4007-9eeb-4029-91d8-b51cda2c1f3a',
    "id_servico": 1,    # 1=Entrega, 4=Reversa, 7=Entrega na Loja, 8=Lotação, 9=Retira
    #   "numero_carga": "2",      
    #                     
    "encomendas": [
        {
          # É o campo no json "id_produto" que corresponde ao tipo de transporte.
          # Exemplo: Expresso, Econômico, etc.
          # Os códigos devem ser solicitados à transportadora.
          # Cada transportadora tem o seu código e produto específico.
          "id_produto": 0,   
          "numero_pedido": "dato123",
          # "data_agendamento": "05/11/2020",
          # "hora_agendamento": "10:00",
          # "nome_marca": null,
          # "data_prevista_entrega": "05/11/2020",
          # "numero_rastreio_embarcador": "ABC123456",
          # "codigo_objeto": "DR125134225BR",
          # "cnpj_unidade_destino": "",
          # "codigo_unidade_destino": null,
          # "metros_cubicos": 0.200,
          # "pedido_integracao": "",
          # "pedido_aguardando_faturamento": false,

          "documento_transportado": {
            # 1 = NF-e (Nota Fiscal Eletrônica)
            # 2 = NFC (Nota Fiscal ao Consumidor)
            # 3 = Declaração
            "tipo": "3", 
            "numero": "644936",
            "quantidade_volumes": "1",
            "valor_documento": 20.00
            # "serie": "65",
            # "chave_acesso": "31200514055516000814550650010415031006468477",
            # "data_emissao": "13/05/2020"
          },

          # "frete_embarcador": {
          #   "frete": 130.00,
          #   "imposto": 5.80,
          #   "frete_total": 135.80
          # },

          "embarcador": {
            "cnpj": "02.891.567/0002-01",
            "razao_social": "SUBWAY SYSTEMS DO BRASIL LTDA",
            # "inscricao_estadual": "373.091.203.117",
            "endereco": {
              "cep": "83412-585",
              "bairro": "Canguiri",
              "rua": "Pedro Zanetti",
              "numero": "230",
              "complemento": "Barracão 2",
              "cidade": "Colombo",
              "estado": "PR"
            }
          },

            "tomador": {
              "cnpj": "08.806.647/0001-17",
              "inscricao_estadual": "9040355992",
              "razao_social": "Amplo Logistica e Armazenagem Ltda",
              "endereco": {
                "cep": "83412-585",
                "bairro": "Canguiri",
                "rua": "Pedro Zanetti",
                "numero": "230",
                "complemento": "Barracão 2",
                "cidade": "Colombo",
                "estado": "PR"
              }
          },

          "destinatario": {
              "tipo_pessoa": "F",     # F = Pessoa Física,  J = Pessoa Jurídica
              "cnpj_cpf": "478.517.310-62",
              # "inscricao_estadual": "",
              "nome": "Dato Amplo",
              "endereco": {
              "cep": "83411-240",
              "bairro": "São Dimas",
              "rua": "Ipê",
              "numero": "1062",
              "complemento": "casa 2",
              "cidade": "Colombo",
              "estado": "PR"
              # "email": "milena.alves@hotmail.com",
              # "telefone": "11912345678",
              # "observacoes": "",
            }
          },

        #   "loja_remetente": {
        #     "cnpj_cpf": "",
        #     "inscricao_estadual": "",
        #     "tipo_pessoa": "F",
        #     "nome": "",
        #     "endereco": {
        #       "cep": "",
        #       "bairro": "",
        #       "rua": "",
        #       "numero": "",
        #       "complemento": "",
        #       "cidade": "",
        #       "estado": ""
        #     }
        #   },

        #   "transportadora_subcontratacao": {
        #     "cnpj": "",
        #     "inscricao_estadual": "",
        #     "razao_social": "",
        #     "endereco": {
        #       "cep": "",
        #       "bairro": "",
        #       "rua": "",
        #       "numero": "",
        #       "complemento": "",
        #       "cidade": "",
        #       "estado": ""
        #     },
        #     "chave_cte": ""
          # },


        # Altura/Largura/Comprimento são campos são do tipo Double em Metros, 
        # para informar centímetro deve se informar 0.010 (um centímetro)
        # Pesos os campos são tipo Double em Kg, para informar grama deve se informar 0.100 (cem gramas)
        #   "volumes": [
        #     {
        #       "codigo_etiqueta": "",
        #       "altura": 0.00,
        #       "largura": 0.00,
        #       "comprimento": 0.00,
        #       "peso_real": 0.00,
        #       "peso_cubado": 0.00
        #     }
        #  ]
        }
      ]
    }
  )
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


