select
	tg.id as id
	, td.contribuinte_id as contribuinte_origem_id
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01') competencia_descricao
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01') data_documento
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01', ' 00:00:00') data_hora_geracao
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01', ' 00:00:00') data_hora_integracao_geracao
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01', ' 00:00:00') data_hora_integracao_alteracao
	, concat(tg.ano, '-', case when tg.mes+1 < 10 then concat('0', tg.mes+1) else tg.mes+1 end, '-', '01', ' 00:00:00') data_hora_integracao_cancelamento
	, vencimento as data_vencimento
	, vencimento as data_vencimento_documento
	, concat(tg.numero, tg.ano, ROW_NUMBER() OVER (ORDER BY tg.numero, tg.ano, tg.id)) as nro_baixa
	, 'NOTA' as sistema_origem
	, case
		when papelServico = 'prestador' then 'SERVICO_PRESTADO'
		when papelServico = 'tomador' then 'SERVICO_TOMADO'
		else papelServico
	end as tipo_guia
	, case
		when tipoBaixa = 'INTEGRACAO' then 'AUTOMATICA'
		when tipoBaixa = 'MANUAL' then 'MANUAL'
		else tipoBaixa
	end as tipo_geracao
	, case
		when dataCancelamento is not null then 'CANCELADA'
		when tg.inscritaDividaAtiva  = 1 then 'INSCRITA_EM_DIVIDA'
		when dataBaixa is not null then 'PAGA'
		else 'ABERTA'
	end as situacao
-- 	, correcao
-- 	, juros
-- 	, multa
	, total as vl_servico
	, case when valorBaixaTotal is null then total else valorBaixaTotal end as vl_guia
	, total as vl_base_calculo
	, total as vl_tributo
	, 0 as  vl_taxa_expediente 
	, 0 as vl_saldo_utilizado
	, 1 as nro_parcela
	, 1 as quantidade_notas
-- 	, valorBaixaJuros
-- 	, valorBaixaMulta
-- 	, valorBaixaPrincipal
-- 	, valorBaixaTaxa
	, td.motivoCancelamento motivo_cancelamento
	, td.dataCancelamento data_hora_cancelamento
	, codBarras as codigo_barras
-- 	, tg.obs
-- 	, pagavel
-- 	, dataBaixa
-- 	, tributo
-- 	, municipioEmissor_id
-- 	, tipoGuia
-- 	, anoDocumento
-- 	, codigo
-- 	, valorBaixaCorrecao
-- 	, valorBaixaDesconto
-- 	, valorInscrito
from
	t_guiaavulsa tg
left join t_documento td on
	td.id = tg.id
-- where numero = 9000221
	-- left join t_evento te on te.id = tg.id
	-- left join t_encerramento te on te.guia_id = tg.id