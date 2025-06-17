def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "listasServicosEntidades": {
                "iListasServicos": item.lista_servico_cloud_id,
                "aliquota": item.aliquota,
                "dtAdesao": item.data_adesao,
                "issDevidoLocalPrest": item.iss_devido_local_prest,
                # "indiceSubstituicao": item.indice_substituicao,
                "permiteAlterarAliquota": item.permite_alterar_aliquota,
                # "indiceDeducao": item.indice_deducao,
                "aliqFederal": item.aliq_federal,
                "aliqEstadual": item.aliq_estadual,
                "aliqMunicipal": item.aliq_municipal,
                # "versaoIbpt": item.versao_ibpt
            }
        }

        if funcao == 'Atualizar':
            dado["listasServicosEntidades"]["idGerado"] = {
            "iEntidades": item.entidade_cloud_id,
            "iListasServicos": item.lista_servico_cloud_id,
            }
        retorno.append(dado)
    return retorno
