def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-portes": {
                "porteEmpresa": item.porte_empresa,
                "dtEfeito": item.data_efeito,
                "idPessoa": item.pessoa_cloud_id
            }
        }

        if item.motivo_cloud_id != None:
            dado = ["pessoas-portes"]["idMotivo"] = item.motivo_cloud_id

        if funcao == 'Atualizar':
            dado["pessoas-portes"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno