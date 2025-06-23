select
	row_number() over () as id
	, serie descricao
	, 'S' as ativa
from
	t_encerramentomemoria
where
	serie is not null
group by
	serie
order by id, serie