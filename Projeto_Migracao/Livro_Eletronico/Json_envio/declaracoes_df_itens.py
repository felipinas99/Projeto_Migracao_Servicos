def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
        "idIntegracao": item.id,
        "declaracoesDfItens": {
            "iDeclaracoes": item.declaracao_cloud_id,
            "iDocumentos": item.documento_cloud_id,
            "iListasServicos": item.lista_servico_cloud_id,
            "iSequencias": item.sequencia_cloud_id,
            "iCnaes": item.cnae_cloud_id,
            "iMunicipios": item.municipio_cloud_id,
            "iIncentivosFiscais": item.incentivo_fiscal_cloud_id,
            "servicoNoPais": item.servico_no_pais,
            "nomeMunicipios": item.nome_municipio,
            "descricaoServico": item.descricao_servico,
            "qtdServico": item.qtd_servico,
            "vlUnitario": item.vl_unitario,
            "vlServico": item.vl_servico,
            "vlDeducao": item.vl_deducao,
            "vlDescIncondicional": item.vl_desc_incondicional,
            "vlDescCondicional": item.vl_desc_condicional,
            "vlBaseCalculo": item.vl_base_calculo,
            "aliquota": item.aliquota,
            "vlIss": item.vl_iss,
            "vlTaxas": item.vl_taxas
        }
    }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno