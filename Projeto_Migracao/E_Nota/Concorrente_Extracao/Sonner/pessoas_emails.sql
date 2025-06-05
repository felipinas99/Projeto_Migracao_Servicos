select
	id as id
	,1 as descricao
	, "SIM" as principal
	, id as pessoa_origem_id
	, email as email
from
	t_pessoa tp where prestador  = 1 and length(email) > 2