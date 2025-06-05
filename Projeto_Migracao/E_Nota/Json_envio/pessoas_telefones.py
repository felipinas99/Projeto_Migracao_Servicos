def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-telefones": {
                "tipo": item.tipo,
                "principal": item.principal,
                "telefone": item.telefone,
                "descricao":item.descricao,
                "observacao": item.observacao,
                "idPessoa": item.pessoa_cloud_id
             }
        }

        if funcao == 'Atualizar':
            dado["pessoas-telefones"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno