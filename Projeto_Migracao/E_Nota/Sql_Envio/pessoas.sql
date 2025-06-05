SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY inscricao ORDER BY id) AS rn
    FROM "E_Nota".pessoas
) sub
WHERE ((inscricao IS NOT NULL AND rn = 1)
   OR inscricao IS null)
and atualizado is null
and id_gerado  is null