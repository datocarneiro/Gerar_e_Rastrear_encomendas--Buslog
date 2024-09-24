# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.authenticate import load_usuario_permitidos
from tkinter import messagebox, filedialog
from export_arquivo.export import exportar_arquivo
import tkinter as tk
import pandas as pd
import requests

# Variável global para armazenar dados do rastreamentoclear
dados_rastreamento = []

def rastrear_objeto(chave_session, usuario, progress):
    global dados_rastreamento

    app = tk.Tk()
    app.withdraw()

    try: 
        if usuario == "":
            messagebox.showinfo("Informação", "Nenhum usuário foi registrado, registre-se")
            return
        
        usuario_formatado = usuario.capitalize()
        
        usuarios_permitidos = load_usuario_permitidos()
        
        if usuario_formatado not in usuarios_permitidos:
            messagebox.showinfo("Informação",
                f'''    *** !!! ATENÇÂO !!! ***\n\n\n
                Usuário: "{usuario_formatado}" sem permissão ! ... \n\n
                Verifique o usuario registrado.\n
                Ou entre em contato com a equipe de TI
            ''')
            return

        file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        
        if not file_path:
            messagebox.showinfo("Informação", "Nenhum arquivo selecionado")
            return
        
        dados = pd.read_excel(file_path, engine='openpyxl')
        total_rows = len(dados)  # Total de linhas para rastrear
        dados_rastreamento.clear()  # Limpa dados anteriores

        messagebox.showinfo("Informação", "Arquivo importado com sucesso")

        progress['maximum'] = total_rows  # Define o valor máximo da barra de progresso

        for i, (coluna_a, coluna_c) in enumerate(zip(dados.iloc[:, 0], dados.iloc[:, 2])):
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
                'Franqui': coluna_a,
                'Tracking': NrNota,
                'DtPrevistaEntrega': DtPrevistaEntrega,
                'Status': status,
                'Data/Hora': Data,
                'NomeRecebedor': NomeRecebedor,
                'Comprovante': CaminhoFoto,
                "LogUsuario": usuario_formatado
            })

            # Atualiza a barra de progresso
            progress['value'] = i + 1  # Atualiza o progresso
            app.update_idletasks()  # Atualiza a interface gráfica

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

    exportar_arquivo(usuario_formatado, dados_rastreamento)