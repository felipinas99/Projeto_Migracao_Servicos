with sp as (select
	max(tr.id) as id
	, tr.contribuinte_id as pessoa_origem_id
	, 'SIM' as optante
from
	t_regimecompetencia tr
left join t_regimeiss tr2 on
	tr2.id = tr.regime_id
where tr2.tipo  = 'Simples'
and ativo = 1
group by 2
)
select
	tp.id
	, tp.id pessoa_origem_id
	, case
		when length(documento) < 12 then 'F'
		when length(documento) < 15 then 'J'
		when length(documento) > 14 then 'J'
		else 'J'
	end as tipo_pessoa
	, case
		when (length(documento) <> 11 and length(documento) <> 14) then null
		else documento
	end as cpf_cnpj
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
	, email as email
	, case when sp.id is not null then 'S' else 'N' end as optante_sn
from
	andradas.t_pessoa tp
left join t_papel p on
	p.ator_id = tp.id
	and p.perfil = 'empresa'
left join t_regimeiss tr on
	tr.id = tp.regimeISS_id
left join sp on tp.id = sp.pessoa_origem_id