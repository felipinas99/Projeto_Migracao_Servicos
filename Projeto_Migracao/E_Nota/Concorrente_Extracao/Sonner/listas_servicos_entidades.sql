select
	id
	, case when cast(codigo as SIGNED) < 10 then concat('0',codigo) else codigo end as codigo
	, descricao
	, aliquota
	, null as listas_servicos_leis_cloud_id
from
	t_grupoatividade
union all
select
	tg.id
	, concat(case when cast(ta.codigo as SIGNED) < 10 then concat('0',ta.codigo) else ta.codigo end ,tg.codigo) as codigo
	, tg.nome as descricao
	, tg.aliquota as aliquota
	, 3 as listas_servicos_leis_cloud_id
from
	t_atividade tg
left join t_grupoatividade ta on
	ta.id = tg.grupo_id