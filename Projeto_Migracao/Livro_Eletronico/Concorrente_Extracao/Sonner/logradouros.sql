select
	id as id
	, cast(nome as char(50)) as nome
	, 98 as tipo_logradouro_cloud_id
	, municipio_id as municipio_origem_id
from
	t_logradouro tl
