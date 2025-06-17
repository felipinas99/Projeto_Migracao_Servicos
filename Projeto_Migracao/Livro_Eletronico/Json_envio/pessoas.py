
def montar(lista, funcao):
    import json
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoa": {
                "celular": item.celular,
                "eMail": item.email,
                "nome": item.nome,
                "nomeFantasia": item.nome_fantasia,
                "telefone": item.telefone,
                "tipoPessoa": item.tipo_pessoa
            }
        }

        if item.inscricao_municipal != None:
            dado["Pessoa"]["inscricaoMunicipal"] =  item.inscricao_municipal

        if item.tipo_pessoa == 'F':
            dado["pessoa"]["pessoaFisica"] = {
                    "cpf": item.cpf_cnpj
                }
            
        if item.tipo_pessoa == 'J':
            dado["pessoa"]["pessoaJuridica"] = {
                    "optanteSimples": item.optante_simples
                }
            if item.cpf_cnpj != None:
                dado["pessoa"]["pessoaJuridica"]["cnpj"] = item.cpf_cnpj

        if item.enderecos != None:
            dado["pessoa"]["enderecos"] = [] 
            for endereco in json.loads(item.enderecos):
                dado["pessoa"]["enderecos"].append( {
                    "codigoBairro": endereco['bairro_cloud_id'],
                    "cep": endereco['cep'],
                    "complemento": endereco['complemento'],
                    "codigoLogradouro": endereco['logradouro_cloud_id'],
                    # "codigoLoteamento": endereco['loteamento_cloud_id'],
                    "codigoMunicipio": endereco['municipio_cloud_id'],
                    "numero": endereco['numero'],
                    "tipoEndereco": endereco['tipo_endereco'],
                    "idPessoa": endereco['pessoa_cloud_id'],
                    # "idTipoEndereco": endereco['tipo_endereco_cloud_id']
                    })



        if funcao == 'Atualizar':
            dado["pessoa"]["idGerado"] = {"iPessoas": item.id_gerado}
        retorno.append(dado)
    return retorno