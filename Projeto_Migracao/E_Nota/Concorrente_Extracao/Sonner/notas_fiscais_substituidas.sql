select id, data_hora_substituicao, motivo_substituicao, contribuinte_origem_id, notas_substituidas_origem_id, notas_substitutas_origem_id from (select
	tn.notaSubstituida_id as id
	, ROW_NUMBER() OVER (PARTITION BY tn.notaSubstituida_id ORDER by tn.notaSubstituida_id) as rn
	, case
		when td.dataCancelamento is null then td.emissao
		else td.dataCancelamento
	end as data_hora_substituicao
	, td.motivoCancelamento as motivo_substituicao
	, tn.prestador_id as contribuinte_origem_id
	, tn.notaSubstituida_id as notas_substituidas_origem_id 
	, tn.id as notas_substitutas_origem_id
from
	t_notafiscal tn
left join t_documento td on
	td.id = tn.id
where
	tn.notaSubstituida_id is not null ) as tab where rn = 1