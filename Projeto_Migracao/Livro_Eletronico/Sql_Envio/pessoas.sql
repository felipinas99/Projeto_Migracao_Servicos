SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cpf_cnpj ORDER BY id) AS rn
    FROM "Livro_Eletronico".pessoas
) sub
WHERE ((cpf_cnpj IS NOT NULL AND rn = 1)
   OR cpf_cnpj IS null)
and atualizado is null
and id_gerado  is null