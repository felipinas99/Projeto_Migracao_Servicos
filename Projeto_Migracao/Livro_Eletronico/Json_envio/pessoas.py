def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoa": {
                "celular": "string",
                "eMail": "string",
                "inscricaoMunicipal": "string",
                "nome": "string",
                "nomeFantasia": "string",
                "pessoaFisica": {
                    "cpf": "string",
                    "idPessoa": 0
                },
                "pessoaJuridica": {
                    "cnpj": "string",
                    "inscricaoEstadual": "string",
                    "optanteSimples": "N",
                    "porteEmpresa": ""
                },
                "telefone": "string",
                "tipoPessoa": "F"
            }
        }

        if funcao == 'Atualizar':
            dado["declarados"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno