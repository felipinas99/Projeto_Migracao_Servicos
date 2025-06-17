with cep_logradouro as (
select
	cep
	, count(*)
	, te.logradouro_id
	, row_number() over (partition by te.logradouro_id
order by
	te.logradouro_id) as rn
from
	t_endereco te
where
	length(te.cep) > 5
group by
	1
	, 3)
select
	id as id
	, cast(nome as char(50)) as nome
	, cep.cep
	, 98 as tipo_logradouro_cloud_id
	, municipio_id as municipio_origem_id
from
	t_logradouro tl
left join cep_logradouro cep on
	cep.logradouro_id = tl.id
	and cep.rn = 1