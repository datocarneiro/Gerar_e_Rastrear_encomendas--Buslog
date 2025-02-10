from authentication.authenticate import load_usuario_permitidos, load_token
from tkinter import messagebox, filedialog
import tkinter as tk
import pandas as pd
import requests
from cotacao.validar_cep import validar_cep
import json
import os

token = load_token()

def realizar_cotação(usuario, progress):
    if usuario == "":
        messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
        return
	
    usuario_formatado = usuario.capitalize()
    usuarios_permitidos = load_usuario_permitidos()
	
    if usuario_formatado not in usuarios_permitidos:
        messagebox.showinfo("Informação", f'''    *** !!! ATENÇÂO !!! ***\n\n\nUsuário: "{usuario_formatado}" sem permissão ! ...\n\nVerifique o usuario registrado.''')
        return

    app = tk.Tk()
    app.withdraw()  # Oculta a janela principal
    file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
    if not file_path:
        messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
        return
    
    messagebox.showinfo("Informação", "Arquivo importado com sucesso")

    try:
        dados = pd.read_excel(file_path, engine='openpyxl')

        cep_corretos = validar_cep(dados.iloc[:, 2])
        print(f'tipo {type(cep_corretos)}cep corretos ::::::::: \n {cep_corretos}')


        total_rows = len(dados)
        progress['maximum'] = total_rows  # Define o valor máximo da barra de progresso

        dados_cotacao = []
        # Correção no loop que gera o payload dinamicamente
        for i, (coluna_a, 
                coluna_b, 
                coluna_c,
                coluna_d,
                coluna_e,
                coluna_f,
                coluna_g,
                coluna_h,
                coluna_i) in enumerate(zip(dados.iloc[:, 0],
                                           dados.iloc[:, 1],
                                           dados.iloc[:, 2],
                                           dados.iloc[:, 3],
                                           dados.iloc[:, 4],
                                           dados.iloc[:, 5],
                                           dados.iloc[:, 6],
                                           dados.iloc[:, 7],
                                           dados.iloc[:, 8])):
            
            franquia = coluna_a
            ordem = coluna_b
            cep_destino = cep_corretos[i]  # Pegando CEP da lista validada
            peso = float(coluna_d)  # Convertendo para float
            valor_mercadoria = float(coluna_e)  # Convertendo para float
            # altura = float(coluna_f)  # Convertendo para float
            # comprimento = float(coluna_g)  # Convertendo para float
            # largura = float(coluna_h)  # Convertendo para float
            # peso_cubado = float(coluna_i)  # Convertendo para float

            print(f'......................................................Progresso: {i+1}/{total_rows} - Ordem: {ordem}..............................................')

            # Atualiza a barra de progresso
            progress['value'] = i + 1  # Atualiza o progresso
            app.update_idletasks()  # Atualiza a interface gráfica

            ############################### ENVIO DO PAYLOAD ############################
            
            
            url = "https://api.track3r.com.br/v2/api/CotacaoFreteIndividual"

            payload = {
                "Token": token,
                "CodigoServico": 1,
                "frete": [
                    {
                        "CepDestino": cep_destino,  # Agora usa o CEP correto
                        "Peso": peso,  # Garante que é float
                        "ValorMercadoria": valor_mercadoria  # Garante que é float
                        # "Altura": 5.1,
                        # "Largura": 5.1,
                        # "Comprimento": 5.1

                    }
                ]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, json=payload)  # Usa 'json' para evitar conversão manual
            response_data = response.json()


            print()
            print(response_data)
            print()

            # Verifica se a chave 'status' está presente e contém dados
            if 'status' in response_data:
                dados_cotacao.append({
                'Franquia': franquia,
                'Ordem': ordem,
                'Cep': cep_destino,
                'ValorFrete': response_data['status'],
                })
                print('entrou no if status, continue')
                continue

            dados_cotacao.append({
                'Franquia': franquia,
                'Ordem': ordem,
                'Cep': cep_destino,
                'Serviço': response_data['frete'][0]['DescricaoProduto'],
                'ValorFrete': response_data['frete'][0]['ValorFrete'],
                'Prazo': response_data['frete'][0]['Prazo'],
            })

    except KeyError as e:
        messagebox.showinfo("Informação", 
			f'''Erro: \n
            Base do arquivo é inválida\n
            {usuario_formatado}, confira o arquivo importado.''')
        return
	
    df = pd.DataFrame(dados_cotacao)

    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)