def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "bairro": {
                "codigoMunicipio":item.municipio_cloud_id,
                "nome": item.nome
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno