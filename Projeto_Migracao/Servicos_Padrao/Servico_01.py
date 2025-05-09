def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "conteudo": {
                "nom2e": item.nome,
                # "cpfcnpj": item.cpfcnpj,
                # "dt_nascimento": item.dt_nascimento,
                # "situacao": item.situacao,
                # "teste": {
                    # "ddd": item.id
                # }
            }
        }
        if funcao == 'ATUALIZAR':
            dado["conteudo"]["id"] = dado.id_gerado
            dado["idGerado"] = dado.id_gerado
        retorno.append(dado)
    return retorno