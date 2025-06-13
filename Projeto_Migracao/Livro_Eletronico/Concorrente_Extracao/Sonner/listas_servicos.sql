select
	id
	, case when cast(codigo as SIGNED) < 10 then concat('0',codigo) else codigo end as lista_servico_cloud_id
	, '25.1.F' as versao_ibpt
	, case when aliquota is null then 0 else TRUNCATE(aliquota,4) end as aliquota
-- 	, null as listas_servicos_leis_cloud_id
	, 11865 as entidade_cloud_id
from
	t_grupoatividade
union all
select
	tg.id
	, concat(case when cast(ta.codigo as SIGNED) < 10 then concat('0',ta.codigo) else ta.codigo end ,tg.codigo) as codigo
	, '25.1.F' as versao_ibpt
	, case when tg.aliquota is null then 0 else TRUNCATE(tg.aliquota,4) end as aliquota
-- 	, 3 as listas_servicos_leis_cloud_id
	, 11865 as entidade_cloud_id
from
	t_atividade tg
left join t_grupoatividade ta on
	ta.id = tg.grupo_id