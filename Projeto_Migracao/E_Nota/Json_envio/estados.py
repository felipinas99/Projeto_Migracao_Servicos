def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "estados": {
                "nome": item.nome,
                "uf": item.uf,
                "idPais": item.pais_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["estados"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno