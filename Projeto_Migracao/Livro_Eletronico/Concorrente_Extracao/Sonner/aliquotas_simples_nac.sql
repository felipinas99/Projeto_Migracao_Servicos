select
	tr.id as id
	, tr.dataInicio  as data_inicial_vigencia
	, last_day(tr.dataInicio)  as data_final_vigencia
	, tr.contribuinte_id as pessoa_origem_id
from
	t_regimecompetencia tr
left join t_regimeiss tr2 on
	tr2.id = tr.regime_id
where tr2.tipo  = 'Simples'
and ativo = 1