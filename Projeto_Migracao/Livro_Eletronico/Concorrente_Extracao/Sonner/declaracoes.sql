select 
	 te.id
	, concat(te.ano, '-', case when te.mes + 1 < 10 then concat('0', te.mes + 1) else te.mes + 1 end, '-', '01') competencia_descricao
	, case
		when papel = 'prestador' then 'P'
		when papel = 'tomador' then 'T'
	end as tipo
	, td.contribuinte_id as pessoa_origem_id
	, te.ano as ano_cloud_id
	, case
		when td.dataCancelamento is not null then 'C'
		when tipo = 'Regular' then 'E'
		when tipo = 'SemMovimento' then 'S'
		when tipo = 'Complementar' then 'E'
		when tipo = 'CEM_PORCENTO_RETIDO' then 'E'
	end as situacao
	, case
		when tipoRegime = 'simples' then 'S'
		else 'N'
	end as simplificada	
	, case
		when dataCancelamento is not null then 'C'
		when tg.inscritaDividaAtiva = 1 then 'T'
		when dataBaixa is not null then 'P'
		when tipo = 'SemMovimento' then 'N'
		when guia_id is null  then 'N'
		else  'N'
	end as situacao_guia
	, qtdNFe as qtd_documentos
	, valorDevido as vl_documento
	, valorDevido as vl_servico
	, valorDevido as vl_imposto_guia
	, valorDevido as vl_servico_simplificada
	, 0 as vl_deducao
	, case when td.dataCancelamento is not null then 0 else totalImposto end as vl_imposto
	, case when td.dataCancelamento is not null then 0 else totalImposto end as vl_imposto_simplificada
	, case when td.dataCancelamento is not null then 0 else  totalFaturado end as vl_base_calculo
from
	t_encerramento te
left join t_documento td on
	td.id = te.id
left join t_guiaavulsa tg on 
    tg.id = te.guia_id 

