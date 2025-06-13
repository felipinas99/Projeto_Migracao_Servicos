SELECT 
    id,
    concat(dia,' 00:00:00') AS data_hora_indexador,
    REPLACE(FORMAT(valor, 2), ',', '.') AS valor,
    indice_id AS indexador_origem_id
FROM t_cotacao