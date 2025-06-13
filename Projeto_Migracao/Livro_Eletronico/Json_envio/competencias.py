def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "competencias": {
                "descricao": item.descricao,
                "dtInicial": item.data_inicial,
                "dtFinal": item.data_final,
                "dtVcto": item.data_vencimento
            }
        }

        if funcao == 'Atualizar':
            dado["competencias"]["idGerado"] = {
                "iCompetencias": item.id_gerado,
                "iEntidades": item.entidade_cloud_id
                }
        retorno.append(dado)
    return retorno