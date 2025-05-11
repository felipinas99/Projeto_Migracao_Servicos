def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "conteudo": {
                "nome": item.nome,
                "cpfCnpj": item.cpfcnpj, 
			    "tipoPessoa": "FISICA",
                "ativo": True,
			    "pessoaFisica": {
				    "sexo": "FEMININO"
			    } 
            }
        }
        if funcao == 'ATUALIZAR':
            dado["conteudo"]["id"] = dado.id_gerado
            dado["idGerado"] = dado.id_gerado
        retorno.append(dado)
    return retorno