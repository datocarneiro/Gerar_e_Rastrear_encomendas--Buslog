
def validar_cep(arquivo):

    print(f'arquivo:::::::::::: \n {arquivo}')

    lista_cep = []

    # Iterar sobre o dicionário original
    for chave, valor in enumerate(arquivo):
        try: 
            # Verificar se o valor tem 7 dígitos
            if len(str(valor)) < 7:
                # Acrescentar o zero no início e o caractere "-" entre os dígitos 6 e 7
                valor_modificado = f'Revisar cep: {valor}'
            # Verificar se o valor tem 7 dígitos
            elif len(str(valor)) == 7:
                # Acrescentar o zero no início e o caractere "-" entre os dígitos 6 e 7
                valor_modificado = '0' + str(valor)[:4] + '-' + str(valor)[4:]
            # Verificar se o valor tem 8 dígitos
            elif len(str(valor)) == 8:
                # Acrescentar o caractere "-" entre os dígitos 5 e 6
                valor_modificado = str(valor)[:5] + '-' + str(valor)[5:]
            else:
                # Valor inválido, mantém o valor original
                valor_modificado = valor

            print(valor_modificado)
            lista_cep.append(valor_modificado)

        except Exception as e:
            print(f'erro: {e}')
            raise f'Linha {chave+1}, Cep {valor}, incorreto'
    return lista_cep

