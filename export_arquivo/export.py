from authentication.authenticate import load_usuario_permitidos
from tkinter import messagebox, filedialog
import pandas as pd

def exportar_arquivo(usuario='', dados_rastreamento=[]):
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
    
    if not dados_rastreamento:
        messagebox.showinfo("Informação", "Nenhum dado para exportar")
        return
    
    df = pd.DataFrame(dados_rastreamento)
    export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
    if export_file_path:
        df.to_excel(export_file_path, index=False)
        messagebox.showinfo("Informação", f"Arquivo exportado com sucesso para:\n\n{export_file_path}")

