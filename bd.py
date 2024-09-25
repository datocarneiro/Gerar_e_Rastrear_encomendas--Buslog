import sqlite3
import pandas as pd

# Reabrir a conexão
conn = sqlite3.connect('meu_banco_de_dados.sqlite')

# Ler os dados da tabela 'encomendas' para um DataFrame
df_lido = pd.read_sql_query(
    # "SELECT * FROM encomendas", 

    "DROP meu_banco_de_dados"

    
    
    conn)

# Fechar a conexão
conn.close()

# Exibir os dados lidos
print("\nDados lidos do banco de dados:")
print(df_lido)
