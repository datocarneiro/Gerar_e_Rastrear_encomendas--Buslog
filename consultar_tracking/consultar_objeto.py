import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gerar_encomenda.m_gerar_encomenda import enviarobjeto
import requests
import pandas as pd
import tkinter as tk
from tkinter import * 


# Variável global para armazenar dados do rastreamento
dados_rastreamento = []

def importar_arquivo(chave_session):
    global dados_rastreamento
    app = tk.Tk()
    app.withdraw()  # Oculta a janela principal
    file_path = tk.filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
    if not file_path:
        tk.messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
        return
    
    dados = pd.read_excel(file_path, engine='openpyxl')
    dados_rastreamento.clear()  # Limpa dados anteriores

    tk.messagebox.showinfo("Informação", "Arquivo importado com sucesso")


    for coluna_a, coluna_c in zip(dados.iloc[:, 0], dados.iloc[:, 2]):
        tracking = str(coluna_c)
        print(tracking, type(tracking))
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
        print(response_data)
        
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

    

    tk.messagebox.showinfo("Informação", "Resultado já disponível para exportação")

def exportar_arquivo():
    global dados_rastreamento
    if not dados_rastreamento:
        tk.messagebox.showinfo("Informação", "Nenhum dado para exportar")
        return
    
    df = pd.DataFrame(dados_rastreamento)
    export_file_path = tk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        tk.messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para: {export_file_path}")

def veridficar_usuario(usuario):
    print(f'Usuario "{usuario}" registrado!')

def criar_janela(chave_session):
    app = tk.Tk()
    
    # Define o tamanho da janela
    largura = 1300
    altura = 800
    # Obtém a largura e altura da tela do usuário
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()
    # Calcula a posição x e y para centralizar a janela na tela
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    # Define a geometria da janela
    app.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')

    app.title("BUGLOG: | Gerar encomendas | Rastrear Objetos")
    app.configure(background='#273142')

    # Nome e Input Usuario
    usuario = Label(app, text='Usuário',background='#273142',foreground='#fff', anchor='w')
    usuario.place(x=10,y=20, width=100, height=20)

    input_usuario = Entry(app, background='#dde', foreground='#009',font=5)
    input_usuario.place(x=10,y=50,width=300, height=30,)
 
    btn_gravar_usuario = tk.Button(app, text="Entrar", background='#3f8f57',foreground='#fff', command=lambda:veridficar_usuario(input_usuario.get()), width=10, height=1)
    btn_gravar_usuario.place(x=230,y=85)
    
    # Botão para importar arquivo
    btn_importar = tk.Button(app, text="Rastrear Objetos", background='#dde', font=5, command=lambda: importar_arquivo(chave_session), width=20, height=2)
    btn_importar.pack(pady=40)

    # Botão para importar arquivo
    btn_importar = tk.Button(app, text="Gerar encomendas", background='#dde',font=5,command=lambda: enviarobjeto(chave_session), width=20, height=2)
    btn_importar.pack(pady=40)
    
    # Botão para exportar arquivo
    btn_exportar = tk.Button(app, text="Exportar Arquivo", background='#dde', font=5,command=exportar_arquivo, width=20, height=2)
    btn_exportar.pack(pady=40)
    
    app.mainloop()