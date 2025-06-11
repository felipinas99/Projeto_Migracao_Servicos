WITH RECURSIVE numeros AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numeros WHERE n < 5 -- ajuste 5 para o máximo de splits esperados
)
SELECT
    case when numeros.n > 1 then concat(cast(tt.id as char),'00',numeros.n) else tt.id end  as id
    ,'CELULAR' as tipo
    ,TRIM(REGEXP_SUBSTR(tt.numero, '[^/]+', 1, numeros.n)) as telefone
    ,CASE WHEN principal = 1 THEN 'SIM' ELSE 'NAO' END as principal
    ,pessoa_id pessoa_origem_id
FROM
    t_telefone tt
    LEFT JOIN t_pessoa tp ON tp.id = tt.pessoa_id
    JOIN numeros ON numeros.n <= 1 + LENGTH(tt.numero) - LENGTH(REPLACE(tt.numero, '/', ''))
WHERE
    LENGTH(tt.numero) > 6
    AND tp.prestador = 1
    AND TRIM(REGEXP_SUBSTR(tt.numero, '[^/]+', 1, numeros.n)) IS NOT null
ORDER BY pessoa_id ASC, idx_tel DESC;