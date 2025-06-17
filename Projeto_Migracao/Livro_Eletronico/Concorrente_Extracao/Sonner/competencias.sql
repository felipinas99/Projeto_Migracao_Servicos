SELECT
    ROW_NUMBER() OVER () AS id,
    DATE_FORMAT(tab.data_inicial, '%b/%Y') AS descricao,
    tab.*
FROM (
    WITH RECURSIVE meses AS (
        SELECT
            DATE('1980-01-01') AS data_inicio
        UNION ALL
        SELECT
            DATE_ADD(data_inicio, INTERVAL 1 MONTH)
        FROM
            meses
        WHERE
            data_inicio < '2025-12-01'
    )
    SELECT
        data_inicio AS data_inicial,
        LAST_DAY(data_inicio) AS data_final,
        DATE_ADD(LAST_DAY(data_inicio), INTERVAL 1 MONTH) AS data_vencimento
    FROM
        meses
) AS tab;