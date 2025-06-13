def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "indexadores": {
                "descricao":item.descricao,
                "sigla": item.sigla,
                "tipo": item.tipo,
                "moedaCorrente": item.moeda_corrente
            }
        }

        if funcao == 'Atualizar':
            dado["indexadores"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno