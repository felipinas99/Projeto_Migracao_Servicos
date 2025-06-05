from decimal import Decimal, ROUND_HALF_UP


def montar(lista, funcao):
    retorno = []
    for item in lista:
        guias_dict = {}

        if item.contribuinte_cloud_id is not None:
            guias_dict["idContribuinte"] = item.contribuinte_cloud_id
        if item.convenio_cloud_id is not None:
            guias_dict["idConvenios"] = item.convenio_cloud_id
        if item.competencia_cloud_id is not None:
            guias_dict["idCompetencia"] = item.competencia_cloud_id
        if item.guia_principal_cloud_id is not None:
            guias_dict["idGuiaPrincipal"] = item.guia_principal_cloud_id
        if item.data_hora_geracao is not None:
            guias_dict["dhGeracao"] = item.data_hora_geracao
        if item.data_hora_integracao_geracao is not None:
            guias_dict["dhIntegracaoGeracao"] = item.data_hora_integracao_geracao
        if item.data_hora_integracao_alteracao is not None:
            guias_dict["dhIntegracaoAlteracao"] = item.data_hora_integracao_alteracao
        if item.data_hora_integracao_cancelamento is not None:
            guias_dict["dhIntegracaoCancelamento"] = item.data_hora_integracao_cancelamento
        if item.data_vencimento is not None:
            guias_dict["dtVencimento"] = item.data_vencimento
        if item.data_documento is not None:
            guias_dict["dtDocumento"] = item.data_documento
        if item.data_vencimento_documento is not None:
            guias_dict["dtVencimentoDocumento"] = item.data_vencimento_documento
        if item.data_validade is not None:
            guias_dict["dtValidade"] = item.data_validade
        if item.nro_parcela is not None:
            guias_dict["nroParcela"] = item.nro_parcela
        if item.nro_baixa is not None:
            guias_dict["nroBaixa"] = item.nro_baixa
        if item.tipo_guia is not None:
            guias_dict["tipoGuia"] = item.tipo_guia
        if item.tipo_geracao is not None:
            guias_dict["tipoGeracao"] = item.tipo_geracao
        if item.sistema_origem is not None:
            guias_dict["sistemaOrigem"] = item.sistema_origem
        if item.situacao is not None:
            guias_dict["situacao"] = item.situacao
        if item.quantidade_notas is not None:
            guias_dict["quantidadeNotas"] = item.quantidade_notas
        if item.nosso_numero is not None:
            guias_dict["nossoNumero"] = item.nosso_numero
        if item.codigo_barras is not None:
            guias_dict["codigoBarras"] = item.codigo_barras
        if item.representacao_numerica is not None:
            guias_dict["representacaoNumerica"] = item.representacao_numerica
        if item.motivo_cancelamento is not None:
            guias_dict["motivoCancelamento"] = item.motivo_cancelamento
        if item.data_hora_cancelamento is not None:
            guias_dict["dhCancelamento"] = item.data_hora_cancelamento
        if item.usuario_cancelamento is not None:
            guias_dict["usuarioCancelamento"] = item.usuario_cancelamento
        if item.situacao_registro_bancario is not None:
            guias_dict["situacaoRegistroBancario"] = item.situacao_registro_bancario
        if item.mensagem_registro_bancario is not None:
            guias_dict["mensagemRegistroBancario"] = item.mensagem_registro_bancario
        if item.tipo_operacao_registro_bancario is not None:
            guias_dict["tipoOperacaoRegistroBancario"] = item.tipo_operacao_registro_bancario
        if item.vl_tributo is not None:
            guias_dict["vlTributo"] = Decimal(item.vl_tributo).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_servico is not None:
            guias_dict["vlServico"] = Decimal(item.vl_servico).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_base_calculo is not None:
            guias_dict["vlBaseCalculo"] = Decimal(item.vl_base_calculo).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_taxa_expediente is not None:
            guias_dict["vlTaxaExpediente"] = Decimal(item.vl_taxa_expediente).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_saldo_utilizado is not None:
            guias_dict["vlSaldoUtilizado"] = Decimal(item.vl_saldo_utilizado).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_guia is not None:
            guias_dict["vlGuia"] = Decimal(item.vl_guia).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if item.vl_documento is not None:
            guias_dict["vlDocumento"] = Decimal(item.vl_documento).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        dado = {
            "idIntegracao": item.id,
            "guias": guias_dict
        }

        if funcao == 'Atualizar':
            dado["guias"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno