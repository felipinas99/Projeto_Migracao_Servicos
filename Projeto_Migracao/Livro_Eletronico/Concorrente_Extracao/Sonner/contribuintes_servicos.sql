select
	tv.id as id
	, pessoa_id as pessoa_origem_id
	, atividade_id as lista_servico_origem_id
	, aliquota as aliquota
from
	t_vinculoatividade tv
left join t_pessoa tp on
	tp.id = tv.pessoa_id
where
	tv.fim is null