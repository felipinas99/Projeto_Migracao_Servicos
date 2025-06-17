def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
                "declarados": {
                "iPessoas": item.pessoa_cloud_id,
                "tipoPessoa": item.tipo_pessoa,
                "iPessoasDeclarados": item.pessoa_declarado_cloud_id,
                "iMunicipios": item.municipio_cloud_id,
                "cpfCnpj": item.cpf_cnpj,
                "numeroDocumento": item.numero_documento,
                "inscricaoMunicipal": item.inscricao_municipal,
                "inscricaoEstadual": item.inscricao_estadual,
                "optanteSn": item.optante_sn,
                "porteEmpresa": item.porte_empresa,
                "nome": item.nome,
                "nomeFantasia": item.nome_fantasia,
                "pais": item.pais,
                "municipio": item.municipio,
                "bairro": item.bairro,
                "endereco": item.endereco,
                "numero": item.numero,
                "cep": item.cep,
                "complemento": item.complemento,
                "email": item.email,
                "telefone": item.telefone,
                "site": item.site,
                "celular": item.celular
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno