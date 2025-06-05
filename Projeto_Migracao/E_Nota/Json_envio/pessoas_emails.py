def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-emails": {
                "descricao": item.descricao,
                "principal": item.principal,
                "email": item.email,
                "idPessoa": item.pessoa_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["pessoas-emails"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno