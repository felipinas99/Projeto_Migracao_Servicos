def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "bairros": {
                "nome": item.nome,
                "idMunicipio": item.municipio_cloud_id,
                "padrao": item.padrao
            }
        }

        if funcao == 'Atualizar':
            dado["bairros"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno