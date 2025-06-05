select
	tp.id
	, tp.id as pessoa_origem_id
	,case
		when tr.tipo = 'Isento' then 'SIM'
		when tr.tipo = 'webIssIsento' then 'SIM'
		else 'NAO'
	end as imune
	, 'NAO' as permite_deducao_nf
	, 'NAO' as permite_servico_descontado_nf
	, 'NAO' as permite_rps_manual
	, 'NAO' as permite_rps_eletronico
	, 'NAO' as desconsiderar_taxa_diversa_rps
from
	andradas.t_pessoa tp
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
			
			
			








