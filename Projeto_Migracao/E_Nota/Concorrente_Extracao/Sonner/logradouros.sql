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
	, nome as nome
	, cep.cep
	, case
		when tipo is null then 'rua'
		else tipo
	end as tipo_logradouro_descricao
	, municipio_id as municipio_origem_id
from
	t_logradouro tl
left join cep_logradouro cep on
	cep.logradouro_id = tl.id
	and cep.rn = 1
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