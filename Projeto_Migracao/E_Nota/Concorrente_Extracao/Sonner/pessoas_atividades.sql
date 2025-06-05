select
	id as id
	, id as pessoa_origem_id
	, case
		when situacao = 'ATIVA' then 'ATIVADO'
		when situacao = 'BAIXADA' then 'BAIXA'
		when situacao = 'BLOQUEADA' then 'SUSPENSAO'
		when situacao = 'PARALISADA' then 'SUSPENSAO'
	end as tipo
	, '2025-05-28' data_movimentacao
from
	t_pessoa tp
where
	prestador = 1
	and situacao is not null