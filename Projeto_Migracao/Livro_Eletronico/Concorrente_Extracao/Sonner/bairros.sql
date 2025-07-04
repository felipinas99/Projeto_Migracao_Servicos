select
	 tab.*
	, 'SIM' as padrao
from
	(
	select
		cast( bairro as char(50)) as nome
		, tl.municipio_id as municipio_origem_id
    ,MD5(CONCAT(cast( bairro as char(50)), '-', tl.municipio_id)) AS id
	from
		t_endereco te
	left join t_pessoa tp on
		tp.id = te.pessoa_id
	left join t_logradouro tl on
		tl.id = te.logradouro_id
	where
	 length(te.bairro) > 1 group by bairro
		, tl.municipio_id) as tab 
group by 1,2,3,4