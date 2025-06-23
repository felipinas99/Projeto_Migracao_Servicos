select
	te.id
	, aliquota*100 as aliquota
	, encerramento_id as declaracao_origem_id
	, encerramento_id as documento_origem_id
	, atividade_id as lista_servico_origem_id
	, td.municipio_id as municipio_origem_id
	, 'S' as servico_no_pais
-- 	, exigibilidade
	, descricao as descricao_servico
-- 	, idDocumento
-- 	, incidenciaMunicipio
-- 	, numero
-- 	, retida
	, serie as serie_descricao
	-- , te.tipoDocumento
	, valorBaseCalculo as vl_servico
	, valorBaseCalculo as vl_base_calculo
	, valorImposto as vl_iss
	-- , tipoTributacao_id
from
	t_encerramentomemoria te
left join t_documento td on td.id = te.idDocumento
	
