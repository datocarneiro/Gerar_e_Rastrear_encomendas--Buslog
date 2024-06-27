from authentication.authenticate import autenthicate_sessao as aut
from consultar_tracking.consultar_objeto import consultar_status 
chave_session = 'sem valor'
# Obtem a chave sa sessão
def obter_session():
    global chave_session
    chave_session = aut()
    return f'A chave da sessão é: {chave_session}'

obter_session()
print('='*160)
print(consultar_status(chave_session))
