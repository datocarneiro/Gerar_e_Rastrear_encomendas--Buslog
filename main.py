from authentication.authenticate import authenticate_sessao as aut
from gerar_encomenda.obter_dados_encomenda import buscar_dados_eship
from consultar_tracking.consultar_objeto import criar_janela

def main():
    chave_session = obter_session()
    criar_janela(chave_session)

def obter_session():
    chave_session = aut()
    return chave_session

# def main():
#     dados_eship()

    

if __name__ == "__main__":
    main()
