select 
	a.id as id
    , 11865 as entidade_cloud_id
    , te.encerramento_id as declaracao_origem_id
	, te.idDocumento as documento_origem_id
	, te.idDocumento as documento_cloud_id
    ,ti.atividade_id as lista_servico_origem_id
    ,ti.idx_item + 1 as sequencia_origem_id
    ,ti.idx_item + 1 as sequencia_cloud_id
    ,tn.municipio_id as municipio_origem_id
    ,'S' as servico_no_pais
    ,tm.nome as nome_municipio
    ,replace(REPLACE(cast(ti.descricao as char(2000)), '\\', ''),'/','') as descricao_servico
    ,ti.quantidade as qtd_servico
    ,ti.valorUnitario as vl_unitario
    ,ti.valorUnitario * ti.quantidade as vl_base_calculo
    ,a.aliquota
    ,a.vl_servico
    ,case when td.dataCancelamento is not null then 0 else round((a.vl_servico/100) * a.aliquota,2) end as vl_iss
    ,0 as vl_deducao
    ,ti.webISSValorDesconto as vl_desc_condicional
    ,ti.webISSValorDescontoIncondicional as vl_desc_incondicional
    , 0 as vl_taxas
from
	t_encerramentomemoria te
left join t_notafiscal tn on
	tn.id = te.idDocumento
left join t_documento td on
	td.id = te.idDocumento
left join t_itemnotafiscal ti on
	ti.notaFiscal_id = tn.id
left join t_municipio tm on
	tm.id = tn.municipio_id
left join lateral (
	select
		ti.aliquota * 100 as aliquota
		, ti.valorUnitario * ti.quantidade as vl_servico
		, MD5(concat(te.id,COALESCE(te.idDocumento,0), COALESCE(ti.id,0))) as id
) a on
	true
-- where a.id is not null