def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "contadores": {
                "inscricao": item.inscricao,
                "crc": item.crc
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno