def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "logradouro": {
            # "bairros": [
            #     {
            #     "codigoBairro": 0,
            #     "idLogradouro": 0,
            #     "idBairro": 0
            #     }
            # ],
            "cep": item.cep,
            "codigoMunicipio": item.municipio_cloud_id,
            "nome": item.nome,
            "codigoTipoLogradouro": item.tipo_logradouro_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["logradouro"]["idGerado"] = {"iLogradouros":item.id_gerado}
        retorno.append(dado)
    return retorno