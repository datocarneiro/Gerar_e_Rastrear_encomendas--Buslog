from authentication.authenticate import authenticate_sessao as aut
from consultar_tracking.consultar_objeto import criar_janela

def main():
    chave_session = obter_session()
    criar_janela(chave_session)

def obter_session():
    chave_session = aut()
    return chave_session

if __name__ == "__main__":
    main()
