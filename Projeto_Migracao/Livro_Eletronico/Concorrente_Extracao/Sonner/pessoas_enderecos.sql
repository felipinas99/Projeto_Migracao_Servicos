select
	te.id as id
	, bairro as bairro_descricao
	, cast(cep as char(8)) as cep
	, cast( complemento as char(60) ) as complemento
	, cast(numero as char(8)) as numero
	, 'C'as tipo_endereco
	, case
		when principal = 1 then 'SIM'
		else 'NAO'
	end as principal
	, logradouro_id as logradouro_origem_id
	, tl.municipio_id as municipio_origem_id
	, tm.estado_id as estado_origem_id
	, pessoa_id as pessoa_origem_id
from
	t_endereco te
left join t_pessoa tp on
	tp.id = te.pessoa_id
left join t_logradouro tl on
	tl.id = te.logradouro_id
left join t_municipio tm on
	tm.id = tl.municipio_id