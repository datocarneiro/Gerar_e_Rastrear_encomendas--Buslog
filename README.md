# Rastreador de Objeto Buslog - API

Nesse projeto atuei como `Desenvolvedor`, construindo uma aplicação permite autenticar uma sessão via API, importar dados de um arquivo Excel, consultar informações de rastreamento de objetos e exportar os resultados para um novo arquivo Excel. A interface gráfica é implementada usando Tkinter.

Tecnologias aplicadas: Tecnologia: 🎯 Python, API Requests , Pandas, Json, Tkinter.

## Estrutura do Projeto

    ├── authentication/
    │   └── authenticate.py
    ├── consultar_tracking/
    │   └── consultar_objeto.py
    ├── main.py
    ├── .env
    ├── requirements.txt
    └── README.md


![image](https://github.com/datocarneiro/Rastreador_de_Objeto_Buslog-API-/assets/132966071/56e93925-d740-4de7-9f6b-ab8cc294b463)

## Configuração
1. Criar Ambiente Virtual
`python -m venv venv`

3. Instalar Dependências
`pip install -r requirements.txt`

5. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e adicione a variável TOKEN com seu token de autenticação.
`TOKEN=seu_token_aqui`

## Uso
1. Autenticação de Sessão
O módulo authenticate.py lida com a autenticação usando um token armazenado em um arquivo .env.

2. Consultar Rastreamento de Objetos
O módulo consultar_objeto.py lida com a importação e exportação de arquivos Excel, bem como com a consulta dos dados de rastreamento via API.

3. Executar a Aplicação
O arquivo main.py inicializa a aplicação.

Dependências:
requests
pandas
openpyxl
python-dotenv
tkinter.

# Iniciando Fase 2 do projeto - 09/2024
No mes de setembro/2024 iniciamos uma nova faze do projeto (EMISSÃO DE PEDIDO)

Estamos incluindo uma nova funcionalidade ao projeto
estamos trabalhando para realizar as Emissões de pediod de forma automatica para a transportadora

## Objetivo: 
- Ganhar agilidade no processo de operação
- Ganhar tempo em prazo de entrega de curto prazo
- Evitar perda de objetos
- Evitar perda de tempo tentando identificar o objeto com a transportadora
- Evitar que a carga fique parada na Base da transortadora (para realizar operações internas, pois os objetos ja estaão prontos para seguir viajem)

