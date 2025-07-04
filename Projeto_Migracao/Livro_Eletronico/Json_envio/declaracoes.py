def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "declaracoes": {
                "iDeclaracoes": item.declaracao_cloud_id,
                "iPessoas": item.pessoa_cloud_id,
                "iCompetencias": item.competencia_cloud_id,
                "iRetificadas": item.retificada_cloud_id,
                "iRetificadoras": item.retificadora_cloud_id,
                "iAutos": item.auto_cloud_id,
                "iAnos": item.ano_cloud_id,
                "situacao": item.situacao,
                "tipo": item.tipo,
                "simplificada": item.simplificada,
                "operadora": item.operadora,
                "situacaoGuia": item.situacao_guia,
                "qtdDocumentos": item.qtd_documentos,
                "vlDocumento": item.vl_documento,
                "vlServico": item.vl_servico,
                "vlBaseCalculo": item.vl_base_calculo,
                "vlImposto": item.vl_imposto,
                "vlDeducao": item.vl_deducao,
                "vlServicoSimplificada": item.vl_servico_simplificada,
                "vlImpostoSimplificada": item.vl_imposto_simplificada,
                "vlServicoOperadora": item.vl_servico_operadora,
                "vlBaseCalculoOperadora": item.vl_base_calculo_operadora,
                "vlImpostoOperadora": item.vl_imposto_operadora,
                "vlSaldo": item.vl_saldo,
                "optanteSn": item.optante_sn,
                "vlImpostoGuia": item.vl_imposto_guia,
                "vlImpostoGuiaSimpl": item.vl_imposto_guia_simpl,
                "issDiferenciado": item.iss_diferenciado,
                "vlTaxas": item.vl_taxas,
                "aliqSugerida": item.aliq_sugerida,
                "aliqInformada": item.aliq_informada,
                "statusEncerrado": item.status_encerrado,
                "vlImpostoSugerido": item.vl_imposto_sugerido,
                "vlImpostoInformado": item.vl_imposto_informado,
                "vlFatBrutoDeclarado": item.vl_fat_bruto_declarado,
                "vlFatBrutoInformado": item.vl_fat_bruto_informado,
                "permaneceOptanteSn": item.permanece_optante_sn,
                "vlRbt12Informado": item.vl_rbt_12_informado,
                "vlFolhaPgtoInformado": item.vl_folha_pgto_informado,
                "nroDas": item.nro_das,
                "vlIssDas": item.vl_iss_das,
                "vlAliquotaIssDas": item.vl_aliquota_iss_das
            }
        }

        if funcao == 'Atualizar':
            dado["declaracoes"]["idGerado"] = {item.id_gerado}
        retorno.append(dado)
    return retorno