def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-enderecos": {
                "descricao": item.descricao,
                "principal": item.principal,
                "ordem": item.ordem,
                "cep": item.cep,
                "numero": item.numero,
                "bloco": item.bloco,
                "complemento": item.complemento,
                "observacao": item.observacao,
                "apartamento": item.apartamento,
                "idPessoa": item.pessoa_cloud_id,
                "idEstado": item.estado_cloud_id,
                "idMunicipio": item.municipio_cloud_id,
                "idLogradouro": item.logradouro_cloud_id,
                "idCondominios": item.condominio_cloud_id,
                "idLoteamentos": item.loteamento_cloud_id,
                "idDistritos": item.distrito_cloud_id
            }
        }

        if item.bairro_cloud_id !=None:
            dado["pessoas-enderecos"]["idBairro"] = item.bairro_cloud_id

        if funcao == 'Atualizar':
            dado["bairros"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno