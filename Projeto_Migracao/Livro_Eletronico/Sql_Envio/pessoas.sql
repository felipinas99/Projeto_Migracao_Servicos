SELECT 
    p.id,
    case when length(t.celular) < 10 then null else t.celular end as celular,
    case when length(t.telefone) < 10 then null else t.telefone end as telefone,
    p.email,
    p.inscricao_municipal,
    p.inscricao_estadual,
    p.nome,
    p.nome_fantasia,
    p.cpf_cnpj,
    p.optante_simples,
    p.tipo_pessoa,
    p.id_gerado,
    p.mensagem,
    p.atualizado,
    p.enderecos
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cpf_cnpj ORDER BY id) AS rn
    FROM "Livro_Eletronico".pessoas
) p
LEFT JOIN LATERAL (
    SELECT 
        CAST(REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(p.celular, '\s+', '', 'g'),
                '[^0-9]', '', 'g'
            ),
            '^0+', ''
        ) AS varchar(11)) AS celular,
        CAST(REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(p.telefone, '\s+', '', 'g'),
                '[^0-9]', '', 'g'
            ),
            '^0+', ''
        ) AS varchar(11)) AS telefone
) t ON true
WHERE ((p.cpf_cnpj IS NOT NULL AND p.rn = 1) OR p.cpf_cnpj IS NULL)
  AND p.atualizado IS NULL
  AND p.id_gerado IS NULL