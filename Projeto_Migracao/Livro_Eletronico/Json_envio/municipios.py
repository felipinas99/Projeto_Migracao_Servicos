def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "municipio": {
                "codigoEstado": item.estado_cloud_id,
                "nome": item.nome,
                "uf": item.uf
            }
        }

        if funcao == 'Atualizar':
            dado["municipio"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno