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
        if funcao == 'Atualizar':
            dado["conteudo"]["id"] = item.id_gerado
            dado["conteudo"]["pessoaFisica"]["id"] = item.id_gerado
            dado["idGerado"] = item.id_gerado
        retorno.append(dado)
    return retorno