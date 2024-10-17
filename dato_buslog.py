from authentication.authenticate import authenticate_sessao as autenticar
from interface import interface

def main():
    chave_session = obter_session()
    interface(chave_session)

def obter_session():
    chave_session = autenticar()
    return chave_session

if __name__ == "__main__":
    main()

