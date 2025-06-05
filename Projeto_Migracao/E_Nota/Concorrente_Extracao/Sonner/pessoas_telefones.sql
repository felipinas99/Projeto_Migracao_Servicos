select
	tt.id as id
	, 'CELULAR' as tipo
	, numero as telefone
	, case when principal = 1 then 'SIM' else 'NAO' end as principal
	, pessoa_id pessoa_origem_id
from
	t_telefone tt 
	left join t_pessoa tp on tp.id  = tt.pessoa_id
	where length(numero) > 6 and tp.prestador  = 1
order by pessoa_id asc, idx_tel desc