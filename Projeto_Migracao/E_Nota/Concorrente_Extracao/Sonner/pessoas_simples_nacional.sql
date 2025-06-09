select
	tr.id as id
	, tr.dataInicio  as data_inicio
	, tr.dataInicio  as data_efeito
	, 'MUNICIPAL' as orgao
	, tr.contribuinte_id as pessoa_origem_id
	, 'SIM' as optante
from
	t_regimecompetencia tr
left join t_regimeiss tr2 on
	tr2.id = tr.regime_id
where tr2.tipo  = 'Simples'
and ativo = 1