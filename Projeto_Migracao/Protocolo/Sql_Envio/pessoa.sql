SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cpfcnpj ORDER BY id) AS rn
    FROM controle.pessoa
) sub
WHERE ((cpfcnpj IS NOT NULL AND rn = 1)
   OR cpfcnpj IS null)
	and id_gerado  is null