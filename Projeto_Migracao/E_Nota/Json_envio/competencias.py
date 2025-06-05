def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "competencias": {
                "exercicio": item.exercicio,
                "descricao": item.descricao,
                "dtInicial": item.data_inicial,
                "dtFinal": item.data_final,
                "dtVcto": item.data_vencimento
            }
        }

        if funcao == 'Atualizar':
            dado["competencias"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno