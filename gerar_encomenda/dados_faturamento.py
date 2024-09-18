import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.authenticate import load_apikey
import requests
import json

url = "http://amplo.eship.com.br/v2/?funcao=webServiceConsultarDadosVolumesFaturamento"

payload = json.dumps({
  "numeroOrdem": "644936"
})
headers = {
  'Content-Type': 'application/json',
  'api': '56c113c26deeb18c682ba0ccc1796d8d',
  'Cookie': 'amplo=q9nmqhk3o28mt0tdskrchp14r9'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)