def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "contribuintesMovOptante": {
                "iPessoas":  item.pessoa_cloud_id,
                "dtInicio":  item.data_inicio,
                "dtEfeito":  item.data_efeito,
                "descricao":  item.descricao,
                "motivo":  item.motivo,
                "orgao":  item.orgao,
                "optanteSn":  item.optante_sn,
                "mei":  item.mei
            }
        }

        if funcao == 'Atualizar':
            dado["contribuintesMovOptante"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno