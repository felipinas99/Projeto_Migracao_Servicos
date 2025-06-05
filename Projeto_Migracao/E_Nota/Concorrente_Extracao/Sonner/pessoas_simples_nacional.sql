select
	tp.id as id
	, tp.id as pessoa_origem_id
	, '2025-05-28' data_inicio
	, '2025-05-28' data_efeito
	, 'NAO' optante
	, 'MUNICIPAL' as orgao
from
	t_pessoa tp
	left join t_regimeiss tr on tr.id = tp.regimeISS_id
where
	tr.tipo  in('simples')
	and tp.prestador  = 1