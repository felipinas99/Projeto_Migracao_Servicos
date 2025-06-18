def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas": {
                "codigoMunicipio":item.municipio_cloud_id,
                "nome": item.nome
            }
        }

        if funcao == 'Atualizar':
            dado["pessoas"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno