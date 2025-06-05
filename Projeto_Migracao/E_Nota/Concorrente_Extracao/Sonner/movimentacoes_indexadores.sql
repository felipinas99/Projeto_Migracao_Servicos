SELECT 
    id,
    dia AS data_movimentacao,
    REPLACE(FORMAT(valor, 2), ',', '.') AS valor_movimentacao,
    indice_id AS indexador_origem_id
FROM t_cotacao