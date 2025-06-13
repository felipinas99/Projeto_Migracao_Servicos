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
		when tr.tipo = 'Faturamento' then 'H'
		when tr.tipo = 'Estimativa' then 'E'
		when tr.tipo = 'Simples' then 'H'
		when tr.tipo = 'FixoAnual' then 'F'
		when tr.tipo = 'SociedadeProfissional' then 'F'
		when tr.tipo = 'NaoIncide' then 'N'
		else 'F'
	end as enquadramento
	, 'N' as tipo_contribuinte
	, case
		when length(documento) < 12 then 'F'
		when length(documento) < 15 then 'J'
		when length(documento) > 14 then 'J'
		else 'J'
	end as tipo_pessoa
	, case
		when length(documento) < 11 then null
		when length(documento) > 14 then null
		else documento
	end as cpf_cnpj
	, 'N' as escritura_dfp
	, 'N' as escritura_dft
	, 'N' as permite_deducao
	, 'N' as declara_conjugada
	, 'N' as descontado_prefeitura
	, 'N' as permite_taxas_especiais
	, case when sp.id is not null then 'S' else 'N' end as optante_sn
from
	andradas.t_pessoa tp
left join t_regimeiss tr on
	tr.id = tp.regimeISS_id
left join sp on tp.id = sp.pessoa_origem_id




