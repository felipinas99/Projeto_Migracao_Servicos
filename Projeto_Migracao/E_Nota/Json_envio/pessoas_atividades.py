def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-atividades": {
                "tipo": item.tipo,
                "dtMovimentacao": item.data_movimentacao,
                "idPessoa": item.pessoa_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["pessoas-atividades"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno