SELECT 
  id,
  pessoa_origem_id,
  pessoa_cloud_id,
  tipo,
  principal,
  REGEXP_REPLACE(
    REGEXP_REPLACE(
      REGEXP_REPLACE(telefone, '\s+', '', 'g'), -- remove espaços em branco
      '[^0-9]', '', 'g'                        -- remove tudo que não for número
    ), 
    '^0+', ''                                 -- remove zeros à esquerda
  ) AS telefone,
  descricao,
  observacao,
  id_gerado,
  mensagem,
  atualizado
FROM "E_Nota".pessoas_telefones
WHERE id_gerado IS NULL;