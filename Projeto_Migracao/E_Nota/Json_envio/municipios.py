def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
             "municipios": {
                "nome": item.nome,
                "uf": item.uf,
                "idEstado": item.estado_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["municipios"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno