def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas": {
                "codigo": item.id,
                "nome": item.nome,
			    "tipoPessoa": "FISICA"
            }
        }
        if funcao == 'ATUALIZAR':
            dado["conteudo"]["id"] = dado.id_gerado
            dado["idGerado"] = dado.id_gerado
        retorno.append(dado)
    return retorno