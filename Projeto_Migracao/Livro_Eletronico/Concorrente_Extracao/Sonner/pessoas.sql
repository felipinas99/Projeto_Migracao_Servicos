with lista_telefone as (with recursive numeros as (
select
	1 as n
union all
select
	n + 1
from
	numeros
where
	n < 5
	-- ajuste 5 para o máximo de splits esperados
)
select
	TRIM(REGEXP_SUBSTR(tt.numero, '[^/]+', 1, numeros.n)) as telefone
	, pessoa_id pessoa_origem_id
	, row_number() over (partition by pessoa_id
order by
	pessoa_id) as rn
from
	t_telefone tt
left join t_pessoa tp on
	tp.id = tt.pessoa_id
join numeros on
	numeros.n <= 1 + length(tt.numero) - length(replace(tt.numero, '/', ''))
where
	length(tt.numero) > 6
	and TRIM(REGEXP_SUBSTR(tt.numero, '[^/]+', 1, numeros.n)) is not null
order by
	pessoa_id asc
	, idx_tel desc)
select
	tp.id
	, case
		when (length(documento) <> 11
			and length(documento) <> 14) then null
		else documento
	end as cpf_cnpj
	, case
		when length(documento) < 12 then 'F'
		when length(documento) < 15 then 'J'
		when length(documento) > 14 then 'J'
		else 'J'
	end as tipo_pessoa
	, cast(case 
		when length(nome) < 2 then concat('Não Informado ' , cast(tp.id as char))
		when nome is null then concat('Não Informado ', cast(tp.id as char))
		else nome 
	end as CHAR(155)) as nome
	, cast(p.nomeFantasia as char(155)) as nome_fantasia
	, case
		when length(inscMun) < 2 then null
		else inscMun
	end as inscricao_municipal
	, case
		when length(inscEst) < 2 then null
		else inscEst
	end as inscricao_estadual
	, email as email
	, lf1.telefone as telefone
	, lf2.telefone as celular
from
	andradas.t_pessoa tp
left join t_papel p on
	p.ator_id = tp.id
	and p.perfil = 'empresa'
left join lista_telefone as lf1 on
	lf1.pessoa_origem_id = tp.id
	and lf1.rn = 1
left join lista_telefone as lf2 on
	lf2.pessoa_origem_id = tp.id
	and lf2.rn = 2