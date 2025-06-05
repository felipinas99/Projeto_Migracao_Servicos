select
	id as id
	, nome as nome
	, case when tipo is null then 'rua' else tipo end as tipo_logradouro_descricao
	, municipio_id as municipio_origem_id
from
	t_logradouro tl
where
	tl.id in (
	select
		te.logradouro_id
	from
		t_endereco te
	left join t_pessoa tp on
		te.pessoa_id = tp.id
	where
		tp.prestador = 1)
group by
	1