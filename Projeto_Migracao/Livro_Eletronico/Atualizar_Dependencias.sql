

CREATE OR REPLACE FUNCTION "Livro_Eletronico".atualizar_dependencias(servico TEXT, sistema TEXT) RETURNS BOOLEAN AS $$
BEGIN

SET search_path TO "Livro_Eletronico";
SET search_path = "Livro_Eletronico";



IF servico = 'pessoas' THEN
  update "Livro_Eletronico".pessoas p
  set id_gerado = p2.id_gerado
  from "Livro_Eletronico".pessoas p2
  where p2.id_gerado is not null and p.id_gerado is null and p2.cpf_cnpj = p.cpf_cnpj and length(p2.cpf_cnpj) > 5;
END IF;
IF servico = 'municipios' THEN
  UPDATE "Livro_Eletronico".municipios o
  SET estado_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

IF servico = 'bairros' THEN
  UPDATE "Livro_Eletronico".bairros o
  SET municipio_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

IF servico = 'logradouros' THEN
  UPDATE "Livro_Eletronico".logradouros o
  SET municipio_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

UPDATE "Livro_Eletronico".logradouros p
SET id_gerado = p2.id_gerado
FROM (
  SELECT id_gerado, nome, municipio_cloud_id
  FROM "Livro_Eletronico".logradouros
  WHERE id_gerado IS NOT NULL
) p2
WHERE p.id_gerado IS NULL
  AND p2.municipio_cloud_id = p.municipio_cloud_id
  AND public.unaccent(lower(trim(p2.nome))) = public.unaccent(lower(trim(p.nome)));
END IF;


IF servico = 'pessoas_enderecos' THEN
  
  CREATE INDEX if not exists idx_bairros_municipio ON "Livro_Eletronico".bairros (municipio_cloud_id);
  CREATE INDEX if not exists idx_pessoas_enderecos_nulos ON "Livro_Eletronico".pessoas_enderecos (bairro_cloud_id, id_gerado, municipio_cloud_id);


  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET municipio_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET estado_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET pessoa_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET logradouro_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".logradouros p
  WHERE p.id = o.logradouro_origem_id AND o.logradouro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".bairros p
  WHERE p.id = o.bairro_origem_id AND o.bairro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Livro_Eletronico".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM (
      SELECT id_gerado, nome, municipio_cloud_id
      FROM "Livro_Eletronico".bairros
  ) p
  WHERE o.bairro_cloud_id IS NULL
    AND o.id_gerado IS NULL
    AND p.municipio_cloud_id = o.municipio_cloud_id
    AND public.unaccent(trim(p.nome)) ILIKE public.unaccent(trim(o.bairro_descricao));

UPDATE "Livro_Eletronico".pessoas pe
SET enderecos = tab.enderecos
FROM (
    SELECT
        pessoa_cloud_id,
        json_agg(json_build_object(
            'idGerado', json_build_object(
                'iPessoas', pessoa_cloud_id,
                'tipoEndereco', tipo_endereco
            ),
            'cep', cep,
            'complemento', complemento,
            'numero', numero,
            'municipio_cloud_id', municipio_cloud_id,
            'logradouro_cloud_id', logradouro_cloud_id,
            'bairro_cloud_id', bairro_cloud_id,
            'pessoa_cloud_id', pessoa_cloud_id,
            'tipo_endereco', tipo_endereco
        )) AS enderecos
    FROM "Livro_Eletronico".pessoas_enderecos
    GROUP BY pessoa_cloud_id
) AS tab
WHERE tab.pessoa_cloud_id = pe.id_gerado;

END IF;


IF servico = 'indexadores_valores' THEN
  update "Livro_Eletronico".indexadores_valores o
  set indexador_cloud_id = p.id_gerado
  from "Livro_Eletronico".indexadores p 
  where p.id  = o.indexador_origem_id and o.indexador_cloud_id is null and o.id_gerado is null;
end if;

IF servico = 'contribuintes' THEN

  -- Atualiza pessoa_cloud_id
  UPDATE "Livro_Eletronico".contribuintes o
  SET pessoa_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS  NULL;

  -- Atualiza contador_cloud_id
  UPDATE "Livro_Eletronico".contribuintes o
  SET contador_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".contadores p
  WHERE p.id = o.contador_origem_id AND o.contador_cloud_id IS NULL AND o.id_gerado IS  NULL;

  -- Atualiza tipo_cloud_id
  -- UPDATE "Livro_Eletronico".contribuintes o
  -- SET tipo_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".tipos p
  -- WHERE p.id = o.tipo_origem_id AND o.tipo_cloud_id IS NULL AND o.id_gerado IS  NULL;

  -- Atualiza banco_cloud_id
  -- UPDATE "Livro_Eletronico".contribuintes o
  -- SET banco_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".bancos p
  -- WHERE p.id = o.banco_origem_id AND o.banco_cloud_id IS NULL AND o.id_gerado IS  NULL;

  -- Atualiza lista_servico_cloud_id
  -- UPDATE "Livro_Eletronico".contribuintes o
  -- SET lista_servico_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".listas_servicos p
  -- WHERE p.id = o.lista_servico_origem_id AND o.lista_servico_cloud_id IS NULL AND o.id_gerado IS  NULL;

END IF;

IF servico = 'contribuintes_servicos' THEN

  -- Atualiza pessoa_cloud_id
  UPDATE "Livro_Eletronico".contribuintes_servicos o
  SET pessoa_cloud_id = cast(p.id_gerado->>'iPessoas' as int )
  FROM "Livro_Eletronico".contribuintes p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;

  -- Atualiza lista_servico_cloud_id
  UPDATE "Livro_Eletronico".contribuintes_servicos o
  SET lista_servico_cloud_id = p.id_gerado->>'iListasServicos'
  FROM "Livro_Eletronico".listas_servicos p
  WHERE p.id = o.lista_servico_origem_id AND o.lista_servico_cloud_id IS NULL AND o.id_gerado IS NULL;

  -- Atualiza cnae_cloud_id
  -- UPDATE "Livro_Eletronico".contribuintes_servicos o
  -- SET cnae_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".cnaes p
  -- WHERE p.id = o.cnae_origem_id AND o.cnae_cloud_id IS NULL AND o.id_gerado IS  NULL;

END IF;

if servico = 'contribuintes_mov_optante' then
  UPDATE "Livro_Eletronico".contribuintes_mov_optante o
  SET pessoa_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;
end if;


IF servico = 'guias' THEN
  -- Atualiza pessoa_cloud_id
  UPDATE "Livro_Eletronico".guias o
  SET pessoa_cloud_id = cast(p.id_gerado->>'iPessoas' as int )
  FROM "Livro_Eletronico".contribuintes p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND p.id_gerado IS NOT NULL;


  -- Atualiza competencia_cloud_id
  UPDATE "Livro_Eletronico".guias o
  SET competencia_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".competencias p
  WHERE p.id = o.competencia_origem_id AND o.competencia_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  UPDATE "Livro_Eletronico".guias n
  SET competencia_cloud_id = c.id_gerado
  FROM "Livro_Eletronico".competencias c
  WHERE n.competencia_descricao BETWEEN c.data_inicial AND c.data_final
    AND n.competencia_cloud_id IS NULL
    AND competencia_descricao IS NOT NULL
    AND n.id_gerado IS NULL;

END IF;


IF servico = 'tomadores_prestadores' THEN

  -- Atualiza pessoa_cloud_id
  UPDATE "Livro_Eletronico".tomadores_prestadores o
  SET pessoa_cloud_id = cast(p.id_gerado->>'iPessoas' as int )
  FROM "Livro_Eletronico".contribuintes p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND p.id_gerado IS NOT NULL;


  -- Atualiza municipio_cloud_id
  UPDATE "Livro_Eletronico".tomadores_prestadores o
  SET municipio_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND p.id_gerado IS NOT NULL;
END IF;


IF servico = 'declaracoes' THEN
  -- Atualiza pessoa_cloud_id
  UPDATE "Livro_Eletronico".declaracoes o
  SET pessoa_cloud_id = cast(p.id_gerado->>'iPessoas' as int )
  FROM "Livro_Eletronico".contribuintes p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza competencia_cloud_id
  UPDATE "Livro_Eletronico".declaracoes o
  SET competencia_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".competencias p
  WHERE p.id = o.competencia_origem_id AND o.competencia_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  UPDATE "Livro_Eletronico".declaracoes n
  SET competencia_cloud_id = c.id_gerado
  FROM "Livro_Eletronico".competencias c
  WHERE n.competencia_descricao BETWEEN c.data_inicial AND c.data_final
    AND n.competencia_cloud_id IS NULL
    AND competencia_descricao IS NOT NULL
    AND n.id_gerado IS NULL;
END IF;

IF servico = 'declaracoes_df' THEN

  -- Atualiza declaracao_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df o
  SET declaracao_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".declaracoes p
  WHERE p.id = o.declaracao_origem_id AND o.declaracao_cloud_id IS NULL AND p.id_gerado IS NOT NULL;


  -- Atualiza projeto_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET projeto_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".projetos p
  -- WHERE p.id = o.projeto_origem_id AND o.projeto_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza serie_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df o
  SET serie_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".series p
  WHERE p.id = o.serie_origem_id AND o.serie_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  UPDATE "Livro_Eletronico".declaracoes_df o
  SET serie_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".series p
  WHERE p.descricao = o.serie_descricao AND o.serie_cloud_id IS NULL AND p.id_gerado IS NOT NULL;


  -- Atualiza arquivo_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET arquivo_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".arquivos p
  -- WHERE p.id = o.arquivo_origem_id AND o.arquivo_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza contribuinte_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df o
  SET contribuinte_cloud_id = cast(p.id_gerado->>'iPessoas' as int )
  FROM "Livro_Eletronico".contribuintes p
  WHERE p.id = o.contribuinte_origem_id AND o.contribuinte_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza declarado_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET declarado_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".declarados p
  -- WHERE p.id = o.declarado_origem_id AND o.declarado_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza lote_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET lote_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".lotes p
  -- WHERE p.id = o.lote_origem_id AND o.lote_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza retificada_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET retificada_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".declaracoes p
  -- WHERE p.id = o.retificada_origem_id AND o.retificada_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza retificadora_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df o
  -- SET retificadora_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".declaracoes p
  -- WHERE p.id = o.retificadora_origem_id AND o.retificadora_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

END IF;

IF servico = 'declaracoes_df_itens' THEN

  -- Atualiza declaracao_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df_itens o
  SET declaracao_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".declaracoes p
  WHERE p.id = o.declaracao_origem_id AND o.declaracao_cloud_id IS NULL AND p.id_gerado IS NOT NULL;


  -- Atualiza lista_servico_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df_itens o
  SET lista_servico_cloud_id = cast(p.id_gerado->>'iListasServicos' as varchar )
  FROM "Livro_Eletronico".listas_servicos p
  WHERE p.id = o.lista_servico_origem_id AND o.lista_servico_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza cnae_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df_itens o
  -- SET cnae_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".cnaes p
  -- WHERE p.id = o.cnae_origem_id AND o.cnae_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza municipio_cloud_id
  UPDATE "Livro_Eletronico".declaracoes_df_itens o
  SET municipio_cloud_id = p.id_gerado
  FROM "Livro_Eletronico".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

  -- Atualiza incentivo_fiscal_cloud_id
  -- UPDATE "Livro_Eletronico".declaracoes_df_itens o
  -- SET incentivo_fiscal_cloud_id = p.id_gerado
  -- FROM "Livro_Eletronico".incentivos_fiscais p
  -- WHERE p.id = o.incentivo_fiscal_origem_id AND o.incentivo_fiscal_cloud_id IS NULL AND p.id_gerado IS NOT NULL;

END IF;

RETURN true;
END;
$$ LANGUAGE plpgsql;
commit