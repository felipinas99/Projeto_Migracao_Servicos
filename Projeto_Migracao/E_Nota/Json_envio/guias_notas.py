def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "guias-notas": {
                "idGuias": item.guia_cloud_id,
                "idNotasFiscais": item.nota_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["guias-notas"]["idGerado"] = {"id": item.id_gerado} 
        retorno.append(dado)
    return retorno