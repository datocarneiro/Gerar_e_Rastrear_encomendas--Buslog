from tkinter import messagebox, filedialog
import pandas as pd

def base_arquivo():
    base = []
    base.append({
        "FRANQUIA/ORIGEM": 'Not Null',
        "MODAL": '',
        "ORDEM": 'Not Null',
        "STATUS": '',
    })
    
    df = pd.DataFrame(base)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        # messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")

def base_arquivo_cotacao():
    base_cotacao = []
    base_cotacao.append({
        "FRANQUIA/ORIGEM": 'Not Null',
        "ORDEM": 'Not Null',
        "CEP_DESTINO(xxxxx-xxx)": 'Not Null',
        "PESO(kg)": 'Not Null',
        "VALOR_MERCADORIA": 'Not Null',
        "ALTURA (cm)": 'Null',
        "COMPRIMENTO (cm)": 'Null',
        "LARGURA(cm)": 'Null',
        "PESO_CUBADO": 'Null',
    })
    
    df = pd.DataFrame(base_cotacao)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        # messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")

