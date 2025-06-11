select
	tp.id
	, case
		when length(documento) < 11 then null
		when length(documento) > 14 then null
		else documento
	end as cpf_cnpj
	, case
		when length(documento) < 12 then 'F'
		when length(documento) < 15 then 'J'
		when length(documento) > 14 then 'J'
		else 'J'
	end as tipo_pessoa
	, cast(case when length(nome) < 2 then null else nome end as CHAR(155)) as nome
	, cast(p.nomeFantasia as char(155)) as nome_fantasia
	, case
		when length(inscMun) < 2 then null
		else inscMun
	end as inscricao_municipal
	, email as email
from
	andradas.t_pessoa tp
left join t_papel p on
	p.ator_id = tp.id
	and p.perfil = 'empresa'







