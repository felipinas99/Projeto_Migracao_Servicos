SELECT 
    ROW_NUMBER() OVER (ORDER BY descricao) AS id,
    descricao
FROM (
    SELECT tipo as descricao
    FROM t_logradouro tl
    WHERE tipo IS NOT NULL
    GROUP BY descricao
) AS sub