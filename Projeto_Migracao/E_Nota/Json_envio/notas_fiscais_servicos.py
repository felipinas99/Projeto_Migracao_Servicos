from decimal import ROUND_HALF_UP, Decimal


def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "notas-fiscais-servicos": {
                "idNotaFiscal": item.nota_fiscal_cloud_id,
                "descontadoPrefeitura": item.descontado_prefeitura,
                "idCnaes": item.cnae_cloud_id,
                "descricaoCnae": item.descricao_cnae,
                "idListasServicosEntidades": item.lista_servico_entidade_cloud_id,
                "descricaoListasServicosEntidades": item.descricao_lista_servico_entidade,
                "aliquota": item.aliquota.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                "prestadoPais": item.prestado_pais,
                "idPaises": item.pais_cloud_id,
                "idMunicipios": item.municipio_cloud_id,
                "discriminacao": item.discriminacao,
                "vlServico": item.vl_servico,
                "quantidade": item.quantidade,
                "vlTotalServico": item.vl_total_servico,
                "vlDescontoCondicionado": item.vl_desconto_condicionado,
                "vlDescontoIncondicionado": item.vl_desconto_incondicionado,
                "vlDeducao": item.vl_deducao,
                "vlBaseCalculo": item.vl_base_calculo,
                "vlIss": item.vl_iss,
                "vlIssOutros": item.vl_iss_outros,
                "aliquotaIbpt": item.aliquota_ibpt,
                "aliquotaIbptFederal": item.aliquota_ibpt_federal,
                "aliquotaIbptEstadual": item.aliquota_ibpt_estadual,
                "aliquotaIbptMunicipal": item.aliquota_ibpt_municipal,
                "vlTributoFederal": item.vl_tributo_federal,
                "vlTributoEstadual": item.vl_tributo_estadual,
                "vlTributoMunicipal": item.vl_tributo_municipal,
                "fonteIbpt": item.fonte_ibpt,
                "codigoTabela": item.codigo_tabela,
                "tabelaPadrao": item.tabela_padrao,
                "anexo": item.anexo,
                "faixa": item.faixa,
                "faturamentoInicial": item.faturamento_inicial,
                "faturamentoFinal": item.faturamento_final,
                "vlRbt12": item.vl_rbt12,
                "rbt12MesAnterior": item.rbt12_mes_anterior,
                "vlSomaRbt12Meses": item.vl_soma_rbt12_meses,
                "vlSomaFolha12Meses": item.vl_soma_folha_12_meses,
                "vlFolhaPgto12": item.vl_folha_pgto_12,
                "percGastoFolha": item.perc_gasto_folha,
                "descricaoReceitaBruta": item.descricao_receita_bruta,
                "descricaoBeneficioFiscal": item.descricao_beneficio_fiscal,
                "tipoBeneficioFiscal": item.tipo_beneficio_fiscal,
                "aplicacaoIncentivo": item.aplicacao_incentivo,
                "percentualReducao": item.percentual_reducao,
                "aliquotaOriginal": item.aliquota_original.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                "vlBaseCalculoOriginal": item.vl_base_calculo_original,
                "vlIssOriginal": item.vl_iss_original,
                "idMunicipiosIncidencia": item.municipio_incidencia_cloud_id
                # "idScript": item.script_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["notas-fiscais-servicos"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno