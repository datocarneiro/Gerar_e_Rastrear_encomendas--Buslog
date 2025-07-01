import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuração do Selenium para rodar em modo headless
chrome_options = Options()
# chrome_options.add_argument("--headless")  # sem abrir janela
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Instala automaticamente o chromedriver compatível
service = Service(ChromeDriverManager().install())

# Cria o driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Lê a planilha de entrada
df = pd.read_excel("cnpjs.xlsx")  # ajuste o nome do arquivo se precisar

# Cria colunas para guardar os resultados
df["IE_SP"] = ""
df["IE_PR"] = ""
df["IE_RJ"] = ""

for index, row in df.iterrows():
    cnpj = str(row["CNPJ"]).zfill(14).replace(".", "").replace("/", "").replace("-", "")
    print(f"Consultando CNPJ: {cnpj}")

    # -------- SINTEGRA SP --------
    try:
        driver.get("https://www.sintegra.fazenda.sp.gov.br/")
        time.sleep(2)
        # Ajuste: localize o campo correto pelo nome, id ou xpath real do site
        input_cnpj = driver.find_element(By.NAME, "cnpj")  # exemplo fictício
        input_cnpj.send_keys(cnpj)
        input_cnpj.send_keys(Keys.RETURN)
        time.sleep(3)
        resultado = driver.find_element(By.XPATH, "//table//td[contains(text(),'Inscrição Estadual')]/following-sibling::td")
        df.at[index, "IE_SP"] = resultado.text.strip()
    except Exception as e:
        print(f"Erro SP: {e}")
        df.at[index, "IE_SP"] = "Erro"

    # -------- SINTEGRA PR --------
    try:
        driver.get("http://www.sintegra.fazenda.pr.gov.br/")
        time.sleep(2)
        input_cnpj = driver.find_element(By.NAME, "cnpj")  # ajuste conforme site real
        input_cnpj.send_keys(cnpj)
        input_cnpj.send_keys(Keys.RETURN)
        time.sleep(3)
        resultado = driver.find_element(By.XPATH, "//table//td[contains(text(),'Inscrição Estadual')]/following-sibling::td")
        df.at[index, "IE_PR"] = resultado.text.strip()
    except Exception as e:
        print(f"Erro PR: {e}")
        df.at[index, "IE_PR"] = "Erro"

    # -------- SINTEGRA RJ --------
    try:
        driver.get("http://www.fazenda.rj.gov.br/projetoSintegra/")
        time.sleep(2)
        input_cnpj = driver.find_element(By.NAME, "cnpj")  # ajuste conforme site real
        input_cnpj.send_keys(cnpj)
        input_cnpj.send_keys(Keys.RETURN)
        time.sleep(3)
        resultado = driver.find_element(By.XPATH, "//table//td[contains(text(),'Inscrição Estadual')]/following-sibling::td")
        df.at[index, "IE_RJ"] = resultado.text.strip()
    except Exception as e:
        print(f"Erro RJ: {e}")
        df.at[index, "IE_RJ"] = "Erro"

# Salva os resultados
df.to_excel("resultado_cnpjs.xlsx", index=False)

driver.quit()
print("Consulta finalizada! Resultados salvos em 'resultado_cnpjs.xlsx'")
