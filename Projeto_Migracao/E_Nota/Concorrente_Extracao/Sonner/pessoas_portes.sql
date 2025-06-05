select
	tp.id as id
	, tp.id as pessoa_origem_id
	, case when tr.tipo = 'MEI' then 'MICROEMPREENDEDOR_MEI' end as porte_empresa 
	, '2025-05-27' as data_efeito
from
	t_pessoa tp
	left join t_regimeiss tr on tr.id = tp.regimeISS_id
where
	tr.tipo  in('MEI')
	and tp.prestador  = 1