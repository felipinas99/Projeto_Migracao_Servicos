select ti.id as id 
,ti.aliquota as aliquota_original
,ti.aliquota as aliquota
-- , case when base is not null then base else end as valor
,cast(descricao as char(2000)) as discriminacao
, 0 as vl_iss
, 0 as vl_iss_outros
, atividade_id as lista_servico_entidade_origem_id
, notaFiscal_id as nota_fiscal_origem_id
, quantidade as quantidade
, valorUnitario as vl_servico
, valorUnitario  * quantidade as vl_total_servico
, valorUnitario  * quantidade as vl_base_calculo
, valorUnitario  * quantidade as vl_base_calculo_original
from t_itemnotafiscal ti 