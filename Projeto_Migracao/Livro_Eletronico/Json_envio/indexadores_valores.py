def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "indexadoresValores": {
                "iIndexadores": item.indexador_cloud_id,
                "iDhIndexadores": item.data_hora_indexador,
                "valor": item.valor
            }
        }

        if funcao == 'Atualizar':
            dado["movimentacoes-indexadores"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno