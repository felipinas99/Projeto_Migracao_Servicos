def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "listas-servicos-entidades": {
                "aliquota": item.aliquota,
                "dtAdesao": item.data_adesao,
                "issDevidoLocalPrestacao": item.iss_devido_local_prestacao,
                "incideSubstituicaoTributaria": item.incide_substituicao_tributaria,
                "permiteAlterarAliquota": item.permite_alterar_aliquota,
                "incideDeducao": item.incide_deducao,
                "aliquotaFederal": item.aliquota_federal,
                "aliquotaEstadual": item.aliquota_estadual,
                "aliquotaMunicipal": item.aliquota_municipal,
                "dtInicioVigencia": item.data_inicio_vigencia,
                "dtFimVigencia": item.data_fim_vigencia,
                "versao": item.versao,
                "descricao": item.descricao,
                "codigo": item.codigo,
                "idListasServicosLeis": item.listas_servicos_leis_cloud_id,
                "nivel": item.nivel,
                "desativado": item.desativado
            }
        }

        if funcao == 'Atualizar':
            dado["listas-servicos-entidades"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno