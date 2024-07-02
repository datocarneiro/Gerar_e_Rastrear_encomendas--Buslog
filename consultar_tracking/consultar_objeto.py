import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Variável global para armazenar dados do rastreamento
dados_rastreamento = []

def importar_arquivo(chave_session):
    global dados_rastreamento
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
    if not file_path:
        messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
        return
    
    dados = pd.read_excel(file_path, engine='openpyxl')
    dados_rastreamento.clear()  # Limpa dados anteriores
    
    for coluna_a, coluna_c in zip(dados.iloc[:, 0], dados.iloc[:, 2]):
        chave = chave_session['sessao']
        url = "https://api.track3r.com.br/v2/api/Tracking"
        payload = {
            "Sessao": chave,
            "CodigoServico": 1,
            "DataInicial": "",
            "DataFinal": "",
            "Pedidos": [
                {"NotaFiscal": coluna_c}
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
        
        dados_rastreamento.append({
            'Fraquia': coluna_a,
            'NrNota': NrNota,
            'DtPrevistaEntrega': DtPrevistaEntrega,
            'Status': status,
            'Data/Hora': Data,
            'NomeRecebedor': NomeRecebedor,
            'Comprovante': CaminhoFoto
        })

    messagebox.showinfo("Informação", "Arquivo importado com sucesso")

    messagebox.showinfo("Informação", "Resultado já disponível para exportação")

def exportar_arquivo():
    global dados_rastreamento
    if not dados_rastreamento:
        messagebox.showinfo("Informação", "Nenhum dado para exportar")
        return
    
    df = pd.DataFrame(dados_rastreamento)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para: {export_file_path}")

def criar_janela(chave_session):
    root = tk.Tk()
    root.title("Importar e Exportar Arquivo Excel")
    
    # Define o tamanho da janela
    largura = 600
    altura = 400
    
    # Obtém a largura e altura da tela do usuário
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    
    # Calcula a posição x e y para centralizar a janela na tela
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    # Define a geometria da janela
    root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
    
    # Botão para importar arquivo
    btn_importar = tk.Button(root, text="Carregar Arquivo", command=lambda: importar_arquivo(chave_session), width=20, height=2)
    btn_importar.pack(pady=40)
    
    # Botão para exportar arquivo
    btn_exportar = tk.Button(root, text="Exportar Arquivo", command=exportar_arquivo, width=20, height=2)
    btn_exportar.pack(pady=40)
    
    root.mainloop()