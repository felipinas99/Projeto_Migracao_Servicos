select
	tp.id
	, case
		when length(tp.grpMobiliario ) > 2 then cast(tp.grpMobiliario as SIGNED)
		when length(inscMun) < 2 then tp.id
		else cast(inscMun as SIGNED)
	end as codigo
	, case
		when length(documento) < 11 then null
		when length(documento) > 14 then null
		else documento
	end as inscricao
	, case
		when tp.situacao = 'BAIXADA' then 'BAIXA_ATIVIDADES'
		when tp.situacao = 'ATIVA' then 'EM_ATIVIDADE'
		when tp.situacao = 'BLOQUEADA' then 'SUSPENSAO_ATIVIDADES'
		when tp.situacao = 'PARALISADA' then 'SUSPENSAO_ATIVIDADES'
		else 'EM_ATIVIDADE'
	end as situacao_economico
	, case
		when length(documento) < 12 then 'FISICA'
		when length(documento) < 15 then 'JURIDICA'
		when length(documento) > 14 then 'JURIDICA'
		else 'JURIDICA'
	end as tipo_pessoa
	, cast(case when length(nome) < 2 then null else nome end as CHAR(155)) as nome
	, cast(p.nomeFantasia as char(155)) as nome_social_fantasia
	, case
		when prestador = 1 then 'PRESTADOR'
		else 'TOMADOR'
	end as perfil
	, case
		when length(inscMun) < 2 then null
		else inscMun
	end as inscricao_municipal
	, case
		when tr.tipo = 'Faturamento' then 'HOMOLOGADO'
		when tr.tipo = 'Estimativa' then 'ESTIMADO'
		when tr.tipo = 'Simples' then 'HOMOLOGADO'
		when tr.tipo = 'FixoAnual' then 'FIXO'
		when tr.tipo = 'SociedadeProfissional' then 'FIXO'
		when tr.tipo = 'NaoIncide' then 'NAO_ENQUADRADO'
	end as modalidade_iss
from
	andradas.t_pessoa tp
left join t_papel p on
	p.ator_id = tp.id
	and p.perfil = 'empresa'
left join t_regimeiss tr on
	tr.id = tp.regimeISS_id
where
	(tp.prestador = 1
		or tp.id in (
		select
			prestador_id
		from
			t_notafiscal
		group by
			1)
		or tp.id in (
		select
			td.contribuinte_id
		from
			t_documento td
		group by
			1) )
			
			
			








