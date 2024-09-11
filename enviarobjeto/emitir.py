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
          "numero_pedido": "6647217",
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
            "numero": "4625886",
            "quantidade_volumes": "1",
            "valor_documento": 59.00
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
            "cnpj": "04.403.408/0013-07"
            # "inscricao_estadual": "373.091.203.117",
            # "razao_social": "Embarcador Homologação",
            # "endereco": {
            #   "cep": "06460-100",
            #   "bairro": "Tamboré",
            #   "rua": "Alameda Pucurui",
            #   "numero": "51",
            #   "complemento": "",
            #   "cidade": "Barueri",
            #   "estado": "SP"
            # }
          },

          #   "tomador": {
          #     "cnpj": "14.055.516/0008-14",
          #     "inscricao_estadual": "373.091.203.117",
          #     "razao_social": "EMBARCADOR HOMOLOGAÇÃO",
          #     "endereco": {
          #       "cep": "06460100",
          #       "bairro": "Tamboré",
          #       "rua": "AVENIDA PUCURUI",
          #       "numero": "51",
          #       "complemento": "",
          #       "cidade": "Barueri",
          #       "estado": "SP"
          #     }
          # },

          "destinatario": {
              "tipo_pessoa": "F",     # F = Pessoa Física,  J = Pessoa Jurídica
              "cnpj_cpf": "217.565.328-50",
              # "inscricao_estadual": "",
              "nome": "MILENA ALVES DOS SANTOS",
              "endereco": {
              "cep": "07811-030",
              "bairro": "CHACARAS DAS COLINAS",
              "rua": "ESTRADA PARA PARNAIBA",
              "numero": "15",
              "complemento": "casa",
              "cidade": "Franco da Rocha",
              "estado": "SP"
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