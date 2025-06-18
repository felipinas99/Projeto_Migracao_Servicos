with sp as (
select
	max(tr.id) as id
	, tr.contribuinte_id as pessoa_origem_id
	, 'SIM' as optante
from
	t_regimecompetencia tr
left join t_regimeiss tr2 on
	tr2.id = tr.regime_id
where
	tr2.tipo = 'Simples'
	and ativo = 1
group by
	2
)
select 
	te.id
	, te.id as declaracao_origem_id
	, td.contribuinte_id as contribuinte_origem_id
	, 1 as df_inicial
	, day(LAST_DAY(concat(te.ano, '-', case when te.mes + 1 < 10 then concat('0', te.mes + 1) else te.mes + 1 end, '-', '01'))) df_final
	, cast(td.emissao as date) data_emissao
	, 'N' as tipo
	, case 
		when dataCancelamento is not null then 'C'
		else 'N'
	end as status
	, 'N' as situacao_tributaria
	, 'N' as descontado_prefeitura
	, valorDevido as vl_documento
	, valorDevido as vl_servico
	, totalImposto as vl_imposto
	, totalFaturado as vl_base_calculo
	, 0 as vl_deducao
	, 1 as natureza_operacao
	, case when sp.id is not null then 'S' else 'N' end as optante_sn
	, case
		when length(documento) < 12 then 'F'
		when length(documento) < 15 then 'J'
		when length(documento) > 14 then 'J'
		else 'J'
	end as tipo_pessoa
	, tp.nome
	, case
		when (length(documento) <> 11 and length(documento) <> 14) then null
		else documento
	end as inscricao
from
	t_encerramento te
left join t_documento td on
	td.id = te.id
left join t_guiaavulsa tg on
	tg.id = te.guia_id
left join t_pessoa tp on
	tp.id = td.contribuinte_id
left join sp on
	tp.id = sp.pessoa_origem_id