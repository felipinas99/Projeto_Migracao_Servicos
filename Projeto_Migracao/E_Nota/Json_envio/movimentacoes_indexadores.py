def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "movimentacoes-indexadores": {
                "idIndexadores": item.indexador_cloud_id,
                "dataMovimentacao": item.data_movimentacao,
                "valorMovimentacao": item.valor_movimentacao
            } 
        }

        if funcao == 'Atualizar':
            dado["movimentacoes-indexadores"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno