from authentication.authenticate import authenticate_sessao_embarcador, authenticate_sessao
from interface import interface

def main():
    chave_session = obter_session()
    interface(chave_session)

def obter_session():
    chave_session = authenticate_sessao_embarcador()
    return chave_session

def obter_session_consulta():
    chave_session_consulta = authenticate_sessao()
    return chave_session_consulta

if __name__ == "__main__":
    main()

