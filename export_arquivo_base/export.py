from tkinter import messagebox, filedialog
import pandas as pd

def base_arquivo():
    base = []
    base.append({
        "FRANQUIA": 'Not Null',
        "MODAL": '',
        "ORDEM": 'Not Null',
        "STATUS": '',
    })
    
    df = pd.DataFrame(base)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")

