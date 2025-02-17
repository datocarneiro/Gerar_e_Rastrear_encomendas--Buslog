import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox

# Função para consultar o banco de dados SQLite filtrando pelo valor de "numero_pedido"
def consultar_banco(ordem):
    try:
        # Conexão com o banco de dados SQLite
        conn = sqlite3.connect('banco_de_dados/banco_de_dados_emissao.sqlite')

        # Query SQL para selecionar onde a coluna "numero_pedido" é igual ao valor de ordem
        query = "SELECT * FROM encomendas WHERE numero_pedido = ?"

        # Executa a query passando o argumento "ordem" para filtrar
        cursor = conn.cursor()
        cursor.execute(query, (ordem,))

        # Recupera os dados e converte para DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        # Fecha a conexão
        conn.close()

        # Verifica se o DataFrame está vazio (nenhum resultado encontrado)
        if df.empty:
            raise ValueError(f"Ordem {ordem} não localizada no banco de dados.")

        # Caminho para exportar o arquivo
        export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if export_file_path:
            df.to_excel(export_file_path, index=False)
            return

    except sqlite3.Error as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        messagebox.showinfo("Informação", f"Erro ao consultar o banco de dados: {e}")
        return None

    except ValueError as ve:
        print(ve)
        messagebox.showinfo("Informação", str(ve))
        return None
