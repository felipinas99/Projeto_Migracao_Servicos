def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "series": {
                "iSeries":item.id,
                "descricao": item.descricao,
                "ativa": item.ativa
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno