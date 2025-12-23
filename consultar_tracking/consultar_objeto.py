from tkinter import messagebox, filedialog
import tkinter as tk
import pandas as pd
import requests
import json
import time

from authentication.authenticate import load_usuario_permitidos, authenticate_sessao
from fiscal.docfiscal import get_doc_fiscal

# Variável global para armazenar dados do rastreamento
dados_rastreamento = []

def rastrear_objeto(usuario, progress_label, progress_label_descricao):
    global dados_rastreamento
    dados_rastreamento.clear()  # Limpa dados anteriores
    
    chave_session = authenticate_sessao()
    app = tk.Tk()
    app.withdraw()

    try:
        if not usuario.strip():
            messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
            return
        
        usuario_formatado = usuario.capitalize()
        usuarios_permitidos = load_usuario_permitidos()
        
        if usuario_formatado not in usuarios_permitidos:
            messagebox.showinfo("Informação", f'Usuário "{usuario_formatado}" sem permissão!')
            return

        file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if not file_path:
            messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
            return

        dados = pd.read_excel(file_path, engine='openpyxl')
        total_rows = len(dados)
        messagebox.showinfo("Informação", "Arquivo importado com sucesso")
        

        for i, (coluna_a, coluna_c) in enumerate(zip(dados.iloc[:, 0], dados.iloc[:, 2])):
            if i > 0:
                time.sleep(12)
            if pd.isna(coluna_c) or str(coluna_c).strip().lower() == 'nan':
                print(f"Tracking inválido na linha {i+1}")
                progresso_atual = f"{i+1}/{total_rows}"
                descricao = f"Ordem: {coluna_c} ... Tracking inválido"
                progress_label.config(text=progresso_atual)
                progress_label_descricao.config(text=descricao)
                app.update_idletasks()
                continue

            try:
                tracking = str(coluna_c).strip()
                chave = chave_session.get('sessao', '')

                url = "https://api.track3r.com.br/v2/api/Tracking"
                payload = json.dumps({
                    "Sessao": chave,
                    "CodigoServico": 1,
                    "Pedidos": [
                        {
                            "ChaveNfe": "",
                            "NotaFiscal": tracking,
                            "Encomenda": ""
                        }
                    ]
                })

                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post(url, headers=headers, data=payload)
                print(f"[{i+1}/{total_rows}] Consulta para Tracking {tracking} - Status HTTP: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.json()
                    pedido = response_data.get('Pedidos', [{}])[0]

                    NrNota = pedido.get('NrNota', '')
                    DtPrevistaEntrega = pedido.get('DtPrevistaEntrega', '')
                    ocorrencias = pedido.get('Ocorrencias', [])

                    status = ocorrencias[0].get('Descricao', '') if ocorrencias else 'Sem Ocorrências'
                    Data = ocorrencias[0].get('Data', '') if ocorrencias else ''
                    NomeRecebedor = ocorrencias[0].get('NomeRecebedor', '') if ocorrencias else ''
                    CaminhoFoto = ocorrencias[0].get('CaminhoFoto', '') if ocorrencias else ''

                    numeroCTe, vlPrest, dacte = get_doc_fiscal(tracking)

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
                    print(f"✅ [{i+1}/{total_rows}] Sucesso: Status={status}")

                else:
                    try:
                        response_data = response.json()
                        mensagem_erro = response_data.get('Mensagem', f'HTTP {response.status_code}')
                    except Exception:
                        mensagem_erro = f'HTTP {response.status_code}'

                    dados_rastreamento.append({
                        'Franqui': coluna_a,
                        'Tracking': tracking,
                        'DtPrevistaEntrega': '',
                        'Status': f'Erro API: {mensagem_erro}',
                        'Data/Hora': '',
                        'NomeRecebedor': '',
                        'Comprovante': '',
                        "LogUsuario": usuario_formatado,
                        "NumeroCTe": '',
                        "ValorPrest": '',
                        "Dacte_pdf": ''
                    })
                    print(f"❌ [{i+1}/{total_rows}] Erro API: {mensagem_erro}")

                descricao = f"Ordem: {coluna_c} ... {status if 'status' in locals() else 'Erro'}"

            except Exception as e:
                dados_rastreamento.append({
                    'Franqui': coluna_a,
                    'Tracking': coluna_c,
                    'DtPrevistaEntrega': '',
                    'Status': f'Erro inesperado: {e}',
                    'Data/Hora': '',
                    'NomeRecebedor': '',
                    'Comprovante': '',
                    "LogUsuario": usuario_formatado,
                    "NumeroCTe": '',
                    "ValorPrest": '',
                    "Dacte_pdf": ''
                })
                descricao = f"Ordem: {coluna_c} ... Erro inesperado"
                print(f"❌ [{i+1}/{total_rows}] Erro inesperado ao processar {coluna_c}: {e}")

            progresso_atual = f"{i+1}/{total_rows}"
            progress_label.config(text=progresso_atual)
            progress_label_descricao.config(text=descricao)
            app.update_idletasks()


    
            

    except Exception as e:
        messagebox.showinfo("Informação", f"Erro inesperado: {e}")
        return

    resposta = messagebox.askquestion("Confirmação", f'{usuario_formatado}, deseja exportar o arquivo dos rastreamentos realizados?')
    if resposta == 'no':
        messagebox.showinfo("Informação", "Operação cancelada.")
        return

    df = pd.DataFrame(dados_rastreamento)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")
