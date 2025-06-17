def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "contribuintesServicos": {
                "iPessoas": item.pessoa_cloud_id,
                "iListasServicos": item.lista_servico_cloud_id,
                "iCnaes": item.cnae_cloud_id,
                "aliquota": item.aliquota,
                "servicoPrincipal": item.servico_principal
            }
        }

        if funcao == 'Atualizar':
            dado["contribuintesServicos"]["idGerado"] = {"iContribuintesServicos": item.id_gerado}
        retorno.append(dado)
    return retorno