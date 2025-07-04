SELECT 
    ti.id AS id,
    ti.aliquota AS aliquota_original,
    ti.aliquota AS aliquota,
    replace(REPLACE(CAST(descricao AS CHAR(2000)), '\\', ''),'/','') AS discriminacao,
    0 AS vl_iss,
    0 AS vl_iss_outros,
    atividade_id AS lista_servico_entidade_origem_id,
    ta.nome AS descricao_lista_servico_entidade,
    notaFiscal_id AS nota_fiscal_origem_id,
    quantidade AS quantidade,
    valorUnitario AS vl_servico,
    valorUnitario * quantidade AS vl_total_servico,
    valorUnitario * quantidade AS vl_base_calculo,
    valorUnitario * quantidade AS vl_base_calculo_original
FROM t_itemnotafiscal ti
LEFT JOIN t_atividade ta ON ta.id = ti.atividade_id;