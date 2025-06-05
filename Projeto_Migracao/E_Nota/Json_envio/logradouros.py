def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "logradouros": {
                "nome":  item.nome,
                "cep":  item.cep,
                "idTipoLogradouro":  item.tipo_logradouro_cloud_id,
                "idMunicipio":  item.municipio_cloud_id
            }       
        }

        if funcao == 'Atualizar':
            dado["logradouros"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno