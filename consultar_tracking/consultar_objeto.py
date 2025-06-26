import sys
import os
from authentication.authenticate import load_usuario_permitidos, authenticate_sessao
from fiscal.docfiscal import get_doc_fiscal
from tkinter import messagebox, filedialog
import tkinter as tk
import pandas as pd
import requests

# Variável global para armazenar dados do rastreamentoclear
dados_rastreamento = []

def rastrear_objeto(usuario, progress_label, progress_label_descricao):
    global dados_rastreamento
    
    chave_session = authenticate_sessao()
    app = tk.Tk()
    app.withdraw()

    try: 
        if usuario == "":
            messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
            return
        
        usuario_formatado = usuario.capitalize()
        
        usuarios_permitidos = load_usuario_permitidos()
        
        if usuario_formatado not in usuarios_permitidos:
            messagebox.showinfo("Informação", f'''    *** !!! ATENÇÂO !!! ***\n\n\nUsuário: "{usuario_formatado}" sem permissão ! ...\n\nVerifique o usuario registrado.''')
            return

        file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        
        if not file_path:
            messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
            return
        
        dados = pd.read_excel(file_path, engine='openpyxl')
        total_rows = len(dados)  # Total de linhas para rastrear
        dados_rastreamento.clear()  # Limpa dados anteriores

        messagebox.showinfo("Informação", "Arquivo importado com sucesso")

        # progress['maximum'] = total_rows  # Define o valor máximo da barra de progresso

        for i, (coluna_a, coluna_c) in enumerate(zip(dados.iloc[:, 0], dados.iloc[:, 2])):
            try:
                tracking = str(coluna_c)
            
                chave = chave_session['sessao']
                url = "https://api.track3r.com.br/v2/api/Tracking"
                payload = {
                    "Sessao": chave,
                    "CodigoServico": 1,
                    "DataInicial": "",
                    "DataFinal": "",
                    "Pedidos": [
                        {"NotaFiscal": tracking}
                    ]
                }
                
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                        
                NrNota = response_data['Pedidos'][0]['NrNota']
                DtPrevistaEntrega = response_data['Pedidos'][0]['DtPrevistaEntrega']
                status = response_data['Pedidos'][0]['Ocorrencias'][0]['Descricao']
                Data = response_data['Pedidos'][0]['Ocorrencias'][0]['Data']
                NomeRecebedor = response_data['Pedidos'][0]['Ocorrencias'][0]['NomeRecebedor']
                CaminhoFoto = response_data['Pedidos'][0]['Ocorrencias'][0]['CaminhoFoto']

                numeroCTe, vlPrest, dacte = get_doc_fiscal(tracking)
                
                print(f'Progresso: {i+1}/{total_rows} - Ordem: {coluna_c} - Status: {status}')
                print(f'________________________________________________')

                dados_rastreamento.append({
                    'Franqui': coluna_a,
                    'Tracking': NrNota,
                    'DtPrevistaEntrega': DtPrevistaEntrega,
                    'Status': status,
                    'Data/Hora': Data,
                    'NomeRecebedor': NomeRecebedor,
                    'Comprovante': CaminhoFoto,
                    "LogUsuario": usuario_formatado,
                    "NumeroCTe": numeroCTe,
                    "ValorPrest": vlPrest,
                    "Dacte_pdf": dacte
                })


                 # Atualiza a barra de progresso
                # progress['value'] = i + 1  # Atualiza o progresso
                progress_label.config(text=f"{i+1}/{total_rows}")  # Atualiza o texto do label
                progress_label_descricao.config(text=f"Ordem: {tracking} ...  {status}")  # Atualiza descrição
                app.update_idletasks()  # Atualiza a interface gráfica
            

            except KeyError as e:
                messagebox.showinfo("Informação", f'''*** ATENÇÂO *** !\n\nErro: Tracking {tracking} não localizado!\n\n\n{usuario_formatado}, Confirme se a encomenda realmente existe.''')
                return

    except KeyError as e:
        messagebox.showinfo("Informação", f'''Erro: \n
            Base do arquivo é inválida!\n
            {usuario_formatado}, Confira o arquivo importado.''')
        return

    resposta = messagebox.askquestion("Confirmação",
    f'''*** !!! ATENÇÂO !!! ***\n\n
    {usuario_formatado}, Deseja exporta o arquivo dos ratreamento realizado?\n
    ''')
	
    if resposta == 'no':
        messagebox.showinfo("Informação", "Operação cancelada.")
        return

    df = pd.DataFrame(dados_rastreamento)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")