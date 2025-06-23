SELECT id
,REGEXP_REPLACE(
    REGEXP_REPLACE(
      REGEXP_REPLACE(celular, '\s+', '', 'g'), -- remove espaços em branco
      '[^0-9]', '', 'g'                        -- remove tudo que não for número
    ), 
    '^0+', ''                                 -- remove zeros à esquerda
  ) AS celular
,email
,inscricao_municipal
,inscricao_estadual
,nome
,nome_fantasia
,cpf_cnpj
,optante_simples
,REGEXP_REPLACE(
    REGEXP_REPLACE(
      REGEXP_REPLACE(telefone, '\s+', '', 'g'), -- remove espaços em branco
      '[^0-9]', '', 'g'                        -- remove tudo que não for número
    ), 
    '^0+', ''                                 -- remove zeros à esquerda
  ) AS telefone
,tipo_pessoa
,id_gerado
,mensagem
,atualizado
,enderecos
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cpf_cnpj ORDER BY id) AS rn
    FROM "Livro_Eletronico".pessoas
) sub
WHERE ((cpf_cnpj IS NOT NULL AND rn = 1)
   OR cpf_cnpj IS null)
and atualizado is null
and id_gerado  is null