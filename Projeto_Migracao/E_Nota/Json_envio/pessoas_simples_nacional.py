def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-simples-nacional": {
                "dtInicio": item.data_inicio,
                "dtEfeito": item.data_efeito,
                "optante": item.optante,
                "orgao": item.orgao,
                "idPessoa": item.pessoa_cloud_id,
                "idMotivo": item.motivo_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["pessoas-simples-nacional"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno