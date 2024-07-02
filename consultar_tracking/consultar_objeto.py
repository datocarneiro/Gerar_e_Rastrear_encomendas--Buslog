
import requests
import pandas as pd

lista = [
            360453,
            360878,
            361412,
            360880,
            360275
]
def consultar_status(chave_session):
    global lista
    dados_rastreamento = []
    for nota in lista:
        chave = chave_session['sessao']
        # print(f'valor da chave e cptura: {chave}')
        url = "https://api.track3r.com.br/v2/api/Tracking"
        payload = {
                "Sessao": chave,
                "CodigoServico": 1,
                "DataInicial": "",
                "DataFinal": "",
                "Pedidos": [
                {
                "NotaFiscal": nota
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        response = response.json()
        NrNota = response['Pedidos'][0]['NrNota']
        DtPrevistaEntrega = response['Pedidos'][0]['DtPrevistaEntrega']
        status = response['Pedidos'][0]['Ocorrencias'][0]['Descricao']
        Data = response['Pedidos'][0]['Ocorrencias'][0]['Data']
        NomeRecebedor = response['Pedidos'][0]['Ocorrencias'][0]['NomeRecebedor']
        CaminhoFoto = response['Pedidos'][0]['Ocorrencias'][0]['CaminhoFoto']
        dados_rastreamento.append({
            'NrNota': NrNota,
            'DtPrevistaEntrega': DtPrevistaEntrega,
            'Status': status,
            'Data/Hora': Data,
            'NomeRecebedor': NomeRecebedor,
            'Comprovante': CaminhoFoto
        })
        df = pd.DataFrame(dados_rastreamento)
    return df


