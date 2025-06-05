from decimal import Decimal

def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "notas-fiscais": {
                "idPessoa": item.pessoa_cloud_id,
                "nroNota": item.nro_nota,
                "dhFatoGerador": item.data_hora_fato_gerador,
                "dhEmissao": item.data_hora_emissao,
                "situacao": item.situacao,
                "optanteSimples": item.optante_simples,
                "naturezaOperacao": item.natureza_operacao,
                "situacaoTributaria": item.situacao_tributaria,
                "nroProcessoSuspensao": item.nro_processo_suspensao,
                "nroRps": item.nro_rps,
                "idSeriesRps": item.series_rps_cloud_id,
                "siglaSeriesRps": item.sigla_series_rps,
                "nroLote": item.nro_lote,
                "nroObra": item.nro_obra,
                "nroArt": item.nro_art,
                "observacaoComplementar": item.observacao_complementar,
                "prestadorCodigo": item.prestador_codigo,
                "prestadorMunicipio": item.prestador_municipio,
                "prestadorMunicipioCodigo": item.prestador_municipio_codigo,
                "prestadorTipoPessoa": item.prestador_tipo_pessoa,
                "prestadorInscricao": item.prestador_inscricao,
                "prestadorNome": item.prestador_nome,
                "prestadorNomeSocialFantasia": item.prestador_nome_social_fantasia,
                "prestadorCep": item.prestador_cep,
                "prestadorBairro": item.prestador_bairro,
                "prestadorIdDistrito": item.prestador_distrito_cloud_id,
                "prestadorDistritos": item.prestador_distritos,
                "prestadorLogradouro": item.prestador_logradouro,
                "prestadorNumero": item.prestador_numero,
                "prestadorComplemento": item.prestador_complemento,
                "prestadorEstado": item.prestador_estado,
                "prestadorEmail": item.prestador_email,
                "prestadorSite": item.prestador_site,
                "prestadorTelefone": item.prestador_telefone,
                "prestadorCelular": item.prestador_celular,
                "prestadorFax": item.prestador_fax,
                "prestadorModalidadeIss": item.prestador_modalidade_iss,
                "prestadorPorteEmpresa": item.prestador_porte_empresa,
                "prestadorImune": item.prestador_imune,
                "prestadorResponsavelTributario": item.prestador_responsavel_tributario,
                "idTomador": item.tomador_cloud_id,
                "tomadorCodigo": item.tomador_codigo,
                "tomadorMunicipio": item.tomador_municipio,
                "tomadorMunicipioCodigo": item.tomador_municipio_codigo,
                "tomadorTipoPessoa": item.tomador_tipo_pessoa,
                # "tomadorInscricao": item.tomador_inscricao,
                "tomadorNome": item.tomador_nome,
                "tomadorNomeSocialFantasia": item.tomador_nome_social_fantasia,
                "tomadorCep": item.tomador_cep,
                "tomadorBairro": item.tomador_bairro,
                "tomadorLogradouro": item.tomador_logradouro,
                "tomadorNumero": item.tomador_numero,
                "tomadorComplemento": item.tomador_complemento,
                "tomadorEmail": item.tomador_email,
                "tomadorSite": item.tomador_site,
                "tomadorTelefone": item.tomador_telefone,
                "tomadorCelular": item.tomador_celular,
                "idTomadorPais": item.tomador_pais_cloud_id,
                "tomadorOptanteSimples": item.tomador_optante_simples,
                "tomadorPorteEmpresa": item.tomador_porte_empresa,
                "tomadorDistrito": item.tomador_distrito,
                "idIntermediario": item.intermediario_cloud_id,
                "intermediarioCodigo": item.intermediario_codigo,
                # "intermediarioInscricao": item.intermediario_inscricao,
                "intermediarioNome": item.intermediario_nome,
                # "intermediarioInscricaoMunicipal": item.intermediario_inscricao_municipal,
                "vlPis": item.vl_pis,
                "vlCofins": item.vl_cofins,
                "vlInss": item.vl_inss,
                "vlIr": item.vl_ir,
                "vlCsll": item.vl_csll,
                "vlOutrasRetencoes": item.vl_outras_retencoes,
                "vlAliquotaPis": item.vl_aliquota_pis,
                "vlAliquotaCofins": item.vl_aliquota_cofins,
                "vlAliquotaInss": item.vl_aliquota_inss,
                "vlAliquotaIr": item.vl_aliquota_ir,
                "vlAliquotaCsll": item.vl_aliquota_csll,
                "vlAliquotaOutras": item.vl_aliquota_outras,
                "idPaisServico": item.pais_servico_cloud_id,
                "idMunicipioServico": item.municipio_servico_cloud_id,
                "servicoDescontadoPrefeitura": item.servico_descontado_prefeitura,
                "servicoPrestadoPais": item.servico_prestado_pais,
                "vlTotalServicos": item.vl_total_servicos,
                "vlTotalDescontosCondicionados": item.vl_total_descontos_condicionados,
                "vlTotalDescontosIncondicionados": item.vl_total_descontos_incondicionados,
                "vlTotalDeducoes": item.vl_total_deducoes,
                "vlTotalLiquido": item.vl_total_liquido,
                "vlTotalBaseCalculo": item.vl_total_base_calculo,
                "vlTotalIss": item.vl_total_iss,
                "aliquotaIbptFederal": item.aliquota_ibpt_federal,
                "aliquotaIbptEstadual": item.aliquota_ibpt_estadual,
                "aliquotaIbptMunicipal": item.aliquota_ibpt_municipal,
                "vlTributoFederal": item.vl_tributo_federal,
                "vlTributoEstadual": item.vl_tributo_estadual,
                "vlTributoMunicipal": item.vl_tributo_municipal,
                "protocoloRps": item.protocolo_rps,
                "responsavelRetencao": item.responsavel_retencao,
                "versaoRps": item.versao_rps,
                "rpsForaDoPrazo": item.rps_fora_do_prazo,
                "tipoCertificado": item.tipo_certificado,
                "utilizaAliquotaMunicipal": item.utiliza_aliquota_municipal,
                "integracaoDisponivel": item.integracao_disponivel,
                "pisPasep": item.pis_pasep,
                "situacaoGuia": item.situacao_guia
            }
        }

        if item.competencias_cloud_id != None:
            dado['notas-fiscais']["idCompetencias"] =  item.competencias_cloud_id

        if item.data_hora_emissao_rps != None:
            dado['notas-fiscais']["dhEmissaoRps"] =  item.data_hora_emissao_rps
        
        if item.vl_total_iss_outros != None:
            dado['notas-fiscais']["vlTotalIssOutros"] =  item.vl_total_iss_outros

        if item.rps_data_limite != None:
            dado['notas-fiscais']["rpsDataLimite"] =  item.rps_data_limite

        if item.data_emissao_pis_pasep != None:
            dado['notas-fiscais']["dataEmissaoPisPasep"] =  item.data_emissao_pis_pasep

        if item.tomador_inscricao_municipal != None:
            dado['notas-fiscais']["tomadorInscricaoMunicipal"] =  item.tomador_inscricao_municipal
            
        if item.tomador_inscricao_estadual != None:
            dado['notas-fiscais']["tomadorInscricaoEstadual"] =  item.tomador_inscricao_estadual

        if item.prestador_inscricao_municipal != None:
            dado['notas-fiscais']["prestadorInscricaoMunicipal"] =  item.prestador_inscricao_municipal

        if item.prestador_inscricao_estadual != None:
            dado['notas-fiscais']["prestadorInscricaoEstadual"] =  item.prestador_inscricao_estadual

        if item.nro_verificacao != None:
            dado['notas-fiscais']["nroVerificacao"] =  item.nro_verificacao

        if item.tomador_uf != None:
            dado['notas-fiscais']["tomadorUf"] =  item.tomador_uf

        if funcao == 'Atualizar':
            dado["notas-fiscais"]["idGerado"] = {"id": item.id_gerado}
            

        retorno.append(dado)
    return retorno