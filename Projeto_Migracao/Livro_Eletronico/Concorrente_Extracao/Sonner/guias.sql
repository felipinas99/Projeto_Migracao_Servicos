	select
		tg.id as id
	, td.contribuinte_id as pessoa_origem_id
	, tg.id as numero_baixa
	, vencimento as data_vencimento
	, concat(tg.ano, '-', case when tg.mes + 1 < 10 then concat('0', tg.mes + 1) else tg.mes + 1 end, '-', '01') competencia_descricao
	, concat(tg.ano, '-', case when tg.mes + 1 < 10 then concat('0', tg.mes + 1) else tg.mes + 1 end, '-', '01') data_referencia
	, coalesce(valorBaixaPrincipal, valorInscrito) + coalesce(valorBaixaJuros, juros) + coalesce(valorBaixaMulta, multa) + coalesce(valorBaixaTaxa, 0) + coalesce(valorBaixaCorrecao, correcao) - coalesce(valorBaixaDesconto, 0) as vl_guia
	, coalesce(valorBaixaPrincipal, valorInscrito) + coalesce(valorBaixaJuros, juros) + coalesce(valorBaixaMulta, multa) + coalesce(valorBaixaTaxa, 0) + coalesce(valorBaixaCorrecao, correcao) - coalesce(valorBaixaDesconto, 0) as vl_documento
	, coalesce(valorBaixaPrincipal, valorInscrito) as vl_imposto
	, coalesce(valorBaixaJuros, juros) as vl_juro
	, coalesce(valorBaixaMulta, multa) as vl_multa
	, coalesce(valorBaixaTaxa, 0) as vl_taxa_expediente
	, coalesce(valorBaixaCorrecao, correcao)  as vl_correcao
	, coalesce(valorBaixaDesconto, 0) as vl_desconto
	, case
			when dataCancelamento is not null then 'C'
		when tg.inscritaDividaAtiva = 1 then 'T'
		when dataBaixa is not null then 'P'
		else 'A'
	end as situacao
	, 1 as tipo
	, codBarras as codigo_barras
from
		t_guiaavulsa tg
left join t_documento td on
		td.id = tg.id