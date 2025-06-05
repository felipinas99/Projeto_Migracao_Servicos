def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-perfis": {
                "idPessoa": item.pessoa_cloud_id,
                "imune": item.imune,
                "responsavelTributario": item.responsavel_tributario,
                "permiteDeducaoNf": item.permite_deducao_nf,
                "permiteServicoDescontadoNf": item.permite_servico_descontado_nf,
                "permiteRpsManual": item.permite_rps_manual,
                "permiteRpsEletronico": item.permite_rps_eletronico,
                "desconsiderarTaxaDiversaRps": item.desconsiderar_taxa_diversa_rps,
                "seqNf": item.seq_nf,
                "seqRpsManual": item.seq_rps_manual,
                "seqRpsEletronico": item.seq_rps_eletronico,
                "codigoEconomico":item.codigo_economico
                }
        }

        if funcao == 'Atualizar':
            dado["pessoas-perfis"]["idGerado"] = {"id":item.id_gerado}
        retorno.append(dado)
    return retorno