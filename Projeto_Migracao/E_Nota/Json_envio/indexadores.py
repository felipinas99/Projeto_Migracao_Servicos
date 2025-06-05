def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "indexadores": {
                "descricao": item.descricao,
                "sigla":item.sigla,
                "tipoIndexador": item.tipo_indexador
            }
        }

        if funcao == 'Atualizar':
            dado["indexadores"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno