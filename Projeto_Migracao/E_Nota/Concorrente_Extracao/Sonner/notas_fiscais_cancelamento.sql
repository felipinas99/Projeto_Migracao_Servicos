select
	tn.id
	, tn.id as nota_fiscal_origem_id
	, dataCancelamento as data_hora_cancelamento
	, td.motivoCancelamento as motivo
	, tn.prestador_id  as contribuinte_origem_id
from
	t_notafiscal tn
left join t_documento td on
	td.id = tn.id
where dataCancelamento is not null