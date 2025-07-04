import json


def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
        "idIntegracao": item.id,
        "declaracoesDf": {
            "iDeclaracoes": item.declaracao_cloud_id,
            "iDocumentos": item.documento_cloud_id,
            "iProjetos": item.projeto_cloud_id,
            "iSeries": item.serie_cloud_id,
            "iArquivos": item.arquivo_cloud_id,
            "iContribuintes": item.contribuinte_cloud_id,
            "iDeclarados": item.declarado_cloud_id,
            "iLotes": item.lote_cloud_id,
            "iRetificadas": item.retificada_cloud_id,
            "iRetificadoras": item.retificadora_cloud_id,
            "dfInicial": item.df_inicial,
            "dfFinal": item.df_final,
            "dtEmissao": item.data_emissao,
            "tipo": item.tipo,
            "status": item.status,
            "naturezaOperacao": item.natureza_operacao,
            "situacaoTributaria": item.situacao_tributaria,
            "descontadoPrefeitura": item.descontado_prefeitura,
            "vlDocumento": item.vl_documento,
            "vlServico": item.vl_servico,
            "vlBaseCalculo": item.vl_base_calculo,
            "vlImposto": item.vl_imposto,
            "vlDeducao": item.vl_deducao,
            "vlLiquido": item.vl_liquido,
            "vlPisPasep": item.vl_pis_pasep,
            "vlCofins": item.vl_cofins,
            "vlInss": item.vl_inss,
            "vlIr": item.vl_ir,
            "vlCsll": item.vl_csll,
            "vlOutrasRetencoes": item.vl_outras_retencoes,
            "aliqPisPasep": item.aliq_pis_pasep,
            "aliqCofins": item.aliq_cofins,
            "aliqInss": item.aliq_inss,
            "aliqIr": item.aliq_ir,
            "aliqCsll": item.aliq_csll,
            "aliqOutrasRetencoes": item.aliq_outras_retencoes,
            "nroLivro": item.nro_livro,
            "nroPagina": item.nro_pagina,
            "tipoPessoa": item.tipo_pessoa,
            "inscricao": item.inscricao,
            "nome": item.nome,
            "motivoCanc": item.motivo_cancelamento,
            "origem": item.origem,
            "optanteSn": item.optante_sn,
            "vlTaxas": item.vl_taxas,
            "vlImpostoSugerido": item.vl_imposto_sugerido,
            "vlImpostoInformado": item.vl_imposto_informado
        }
    }

        if funcao == 'Atualizar':
            dado["declaracoesDf"]["idGerado"] = json.loads(item.id_gerado)
        retorno.append(dado)
    return retorno