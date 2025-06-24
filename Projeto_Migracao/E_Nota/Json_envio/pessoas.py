def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas": {
                "codigo": item.codigo,
                "tipoPessoa": item.tipo_pessoa,
                # "inscricaoEstadual": item.inscricao_estadual,
                "nome": item.nome,
                "nomeSocialFantasia": item.nome_social_fantasia,
                # "possuiInscricaoEstadual": item.possui_inscricao_estadual,
                # "orgaoRegistro": item.orgao_registro,
                # "dtRegistro": item.dt_registro,
                # "nroRegistro": item.nro_registro,
                # "funcaoResponsavel": item.funcao_responsavel,
                # "site": item.site,
                # "autorizacaoEmissaoNf": item.autorizacao_emissao_nf,
                # "motivo": item.motivo,
                # "pisPasep": item.pis_pasep,
                # "dataEmissaoPisPasep": item.data_emissao_pis_pasep,
                # "idPessoasPerfis": item.id_pessoas_perfis,
                # "idNaturezaJuridica": item.id_natureza_juridica,
                # "idQualificacao": item.id_qualificacao,
                # "idResponsavel": item.id_responsavel,
                "perfil": item.perfil
            }
        }

        if item.inscricao !=None:
            dado["pessoas"]["inscricao"] = item.inscricao

        if item.inscricao_municipal != None:
            dado["pessoas"]["inscricaoMunicipal"] = item.inscricao_municipal

        if item.inscricao_estadual != None:
            dado["pessoas"]["inscricaoEstadual"] = item.inscricao_estadual

        if item.situacao_economico != None:
            dado["pessoas"]["situacaoEconomico"] = item.situacao_economico
            
        if item.modalidade_iss != None:
            dado["pessoas"]["modalidadeIss"] = item.modalidade_iss

        if funcao == 'Atualizar':
            dado["pessoas"]["idGerado"] ={"id":item.id_gerado } 
        retorno.append(dado)
    return retorno