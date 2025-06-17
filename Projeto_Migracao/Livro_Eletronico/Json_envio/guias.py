def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
             "guias": {
                "iPessoas": item.pessoa_cloud_id,
                "iCompetencias": item.competencia_cloud_id,
                "numeroBaixa": int(item.numero_baixa),
                "dtVcto": item.data_vencimento,
                "dtReferencia": item.data_referencia,
                "vlGuia": item.vl_guia,
                "vlDesconto": item.vl_desconto,
                "vlJuro": item.vl_juro,
                "vlMulta": item.vl_multa,
                "vlCorrecao": item.vl_correcao,
                "vlTaxaExpediente": item.vl_taxa_expediente,
                "vlImposto": item.vl_imposto,
                "situacao": item.situacao,
                "tipo": item.tipo,
                "nossoNumero": item.nosso_numero,
                "representacaoNumerica": item.representacao_numerica,
                "codigoBarras": item.codigo_barras,
                "nroConvenio": item.nro_convenio,
                "nroBanco": item.nro_banco,
                "dtValidade": item.data_validade,
                "vlDocumento": item.vl_documento,
                "dtEmissao": item.data_emissao,
                "dtVctoBoleto": item.data_vencimento_boleto
            }
        }

        if funcao == 'Atualizar':
            dado["guias"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno