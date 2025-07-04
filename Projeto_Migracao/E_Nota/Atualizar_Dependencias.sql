

CREATE OR REPLACE FUNCTION "E_Nota".atualizar_dependencias(servico TEXT, sistema TEXT) RETURNS BOOLEAN AS $$
BEGIN

SET search_path TO sistema;

IF servico = 'pessoas_emails' THEN
  update "E_Nota".pessoas_emails o
  set pessoa_cloud_id = p.id_gerado
  from "E_Nota".pessoas p 
  where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;
end if;

IF servico = 'pessoas_telefones' THEN
  update "E_Nota".pessoas_telefones o
  set pessoa_cloud_id = p.id_gerado
  from "E_Nota".pessoas p 
  where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;
end if;

IF servico = 'movimentacoes_indexadores' THEN
  update "E_Nota".movimentacoes_indexadores o
  set indexador_cloud_id = p.id_gerado
  from "E_Nota".indexadores p 
  where p.id  = o.indexador_origem_id and o.indexador_cloud_id is null and o.id_gerado is null;
end if;


-- municipios
IF servico = 'municipios' THEN
  UPDATE "E_Nota".municipios o
  SET estado_cloud_id = p.id_gerado
  FROM "E_Nota".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- logradouros
IF servico = 'logradouros' THEN
  UPDATE "E_Nota".logradouros o
  SET municipio_cloud_id = p.id_gerado
  FROM "E_Nota".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".logradouros o
  SET tipo_logradouro_cloud_id = p.id_gerado
  FROM "E_Nota".tipos_logradouros p
  WHERE p.id = o.tipo_logradouro_origem_id AND o.tipo_logradouro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".logradouros o
  SET tipo_logradouro_cloud_id = p.id_gerado
  FROM "E_Nota".tipos_logradouros p
  WHERE p.descricao ILIKE o.tipo_logradouro_descricao AND o.tipo_logradouro_cloud_id IS NULL AND o.id_gerado IS NULL;

UPDATE "E_Nota".logradouros p
SET id_gerado = p2.id_gerado
FROM (
  SELECT id_gerado, nome, municipio_cloud_id
  FROM "E_Nota".logradouros
  WHERE id_gerado IS NOT NULL
) p2
WHERE p.id_gerado IS NULL
  AND p2.municipio_cloud_id = p.municipio_cloud_id
  AND public.unaccent(lower(trim(p2.nome))) = public.unaccent(lower(trim(p.nome)));
END IF;

-- bairros
IF servico = 'bairros' THEN
  UPDATE "E_Nota".bairros o
  SET municipio_cloud_id = p.id_gerado
  FROM "E_Nota".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_enderecos
IF servico = 'pessoas_enderecos' THEN
  UPDATE "E_Nota".pessoas_enderecos o
  SET municipio_cloud_id = p.id_gerado
  FROM "E_Nota".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_enderecos o
  SET estado_cloud_id = p.id_gerado
  FROM "E_Nota".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_enderecos o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_enderecos o
  SET logradouro_cloud_id = p.id_gerado
  FROM "E_Nota".logradouros p
  WHERE p.id = o.logradouro_origem_id AND o.logradouro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM "E_Nota".bairros p
  WHERE p.id = o.bairro_origem_id AND o.bairro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM "E_Nota".bairros p
  WHERE unaccent(trim(p.nome)) ILIKE unaccent(trim(o.bairro_descricao))
    AND p.municipio_cloud_id = o.municipio_cloud_id
    AND o.bairro_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_listas_servicos_cnaes
IF servico = 'pessoas_listas_servicos_cnaes' THEN
  UPDATE "E_Nota".pessoas_listas_servicos_cnaes o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_listas_servicos_cnaes o
  SET lista_servico_entidade_cloud_id = p.id_gerado
  FROM "E_Nota".listas_servicos_entidades p
  WHERE p.id = o.lista_servico_entidade_origem_id AND o.lista_servico_entidade_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".pessoas_listas_servicos_cnaes o
  SET codigo_lista_servico_entidade = p.codigo
  FROM "E_Nota".listas_servicos_entidades p
  WHERE p.id_gerado = o.lista_servico_entidade_cloud_id AND o.lista_servico_entidade_cloud_id IS NOT NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_portes
IF servico = 'pessoas_portes' THEN
  UPDATE "E_Nota".pessoas_portes o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_simples_nacional
IF servico = 'pessoas_simples_nacional' THEN
  UPDATE "E_Nota".pessoas_simples_nacional o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_atividades
IF servico = 'pessoas_atividades' THEN
  UPDATE "E_Nota".pessoas_atividades o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- pessoas_perfis
IF servico = 'pessoas_perfis' THEN
  UPDATE "E_Nota".pessoas_perfis o
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

-- notas_fiscais
IF servico = 'notas_fiscais' THEN
  UPDATE "E_Nota".notas_fiscais n
  SET pessoa_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = n.pessoa_origem_id AND n.pessoa_cloud_id IS NULL AND n.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais n
  SET competencias_cloud_id = c.id_gerado
  FROM "E_Nota".competencias c
  WHERE c.id = n.competencias_origem_id AND n.competencias_cloud_id IS NULL AND competencias_origem_id IS NOT NULL AND n.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais n
  SET competencias_cloud_id = c.id_gerado
  FROM "E_Nota".competencias c
  WHERE n.competencias_descricao BETWEEN c.data_inicial AND c.data_final AND n.competencias_cloud_id IS NULL AND competencias_descricao IS NOT NULL AND n.id_gerado IS NULL;

  update "E_Nota".notas_fiscais nf set prestador_telefone = tab.telefone from (select
    pessoa_origem_id
    , cast(REGEXP_REPLACE(
      REGEXP_REPLACE(
        REGEXP_REPLACE(telefone, '\s+', '', 'g'), -- remove espaços em branco
        '[^0-9]', '', 'g'                        -- remove tudo que não for número
      ), 
      '^0+', ''                                 -- remove zeros à esquerda
    ) as varchar(11))as telefone
    , row_number() over (PARTITION by pessoa_origem_id
    order by pessoa_origem_id
    , pt.id) as rn
    from
    "E_Nota".pessoas_telefones pt ) as tab where 
    tab.pessoa_origem_id  = nf.pessoa_origem_id 
    and rn = 1 
    and nf.prestador_telefone  is null;
	
	

  -- UPDATE "E_Nota".notas_fiscais n
  -- SET series_rps_cloud_id = s.id_gerado
  -- FROM "E_Nota".series_rps s
  -- WHERE s.id = n.series_rps_origem_id AND n.series_rps_cloud_id IS NULL AND n.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais n
  -- SET prestador_distrito_cloud_id = d.id_gerado
  -- FROM "E_Nota".distritos d
  -- WHERE d.id = n.prestador_distrito_origem_id AND n.prestador_distrito_cloud_id IS NULL AND n.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais n
  SET tomador_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = n.tomador_origem_id AND n.tomador_cloud_id IS NULL AND n.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais n
  -- SET tomador_pais_cloud_id = p.id_gerado
  -- FROM "E_Nota".paises p
  -- WHERE p.id = n.tomador_pais_origem_id AND n.tomador_pais_cloud_id IS NULL AND n.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais n
  -- SET intermediario_cloud_id = p.id_gerado
  -- FROM "E_Nota".pessoas p
  -- WHERE p.id = n.intermediario_origem_id AND n.intermediario_cloud_id IS NULL AND n.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais n
  -- SET pais_servico_cloud_id = p.id_gerado
  -- FROM "E_Nota".paises p
  -- WHERE p.id = n.pais_servico_origem_id AND n.pais_servico_cloud_id IS NULL AND n.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais n
  SET municipio_servico_cloud_id = m.id_gerado
  FROM "E_Nota".municipios m
  WHERE m.id = n.municipio_servico_origem_id AND n.municipio_servico_cloud_id IS NULL AND n.id_gerado IS NULL;
END IF;

-- notas_fiscais_servicos
IF servico = 'notas_fiscais_servicos' THEN
  UPDATE "E_Nota".notas_fiscais_servicos nfs
  SET nota_fiscal_cloud_id = nf.id_gerado
  FROM "E_Nota".notas_fiscais nf
  WHERE nf.id = nfs.nota_fiscal_origem_id
    AND nfs.nota_fiscal_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais_servicos nfs
  -- SET cnae_cloud_id = c.id_gerado
  -- FROM "E_Nota".cnaes c
  -- WHERE c.id = nfs.cnae_origem_id
  --   AND nfs.cnae_cloud_id IS NULL
  --   AND nfs.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_servicos nfs
  SET lista_servico_entidade_cloud_id = lse.id_gerado
  FROM "E_Nota".listas_servicos_entidades lse
  WHERE lse.id = nfs.lista_servico_entidade_origem_id
    AND nfs.lista_servico_entidade_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais_servicos nfs
  -- SET pais_cloud_id = p.id_gerado
  -- FROM "E_Nota".paises p
  -- WHERE p.id = nfs.pais_origem_id
  --   AND nfs.pais_cloud_id IS NULL
  --   AND nfs.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_servicos nfs
  SET municipio_cloud_id = m.id_gerado
  FROM "E_Nota".municipios m
  WHERE m.id = nfs.municipio_origem_id
    AND nfs.municipio_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_servicos nfs
  SET municipio_incidencia_cloud_id = m.id_gerado
  FROM "E_Nota".municipios m
  WHERE m.id = nfs.municipio_incidencia_origem_id
    AND nfs.municipio_incidencia_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;

  -- UPDATE "E_Nota".notas_fiscais_servicos nfs
  -- SET script_cloud_id = s.id_gerado
  -- FROM "E_Nota".scripts s
  -- WHERE s.id = nfs.script_origem_id
  --   AND nfs.script_cloud_id IS NULL
  --   AND nfs.id_gerado IS NULL;
END IF;

-- notas_fiscais_cancelamento
IF servico = 'notas_fiscais_cancelamento' THEN
  UPDATE "E_Nota".notas_fiscais_cancelamento o
  SET contribuinte_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.contribuinte_origem_id AND o.contribuinte_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_cancelamento nfs
  SET nota_fiscal_cloud_id = nf.id_gerado
  FROM "E_Nota".notas_fiscais nf
  WHERE nf.id = nfs.nota_fiscal_origem_id
    AND nfs.nota_fiscal_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;
END IF;

-- notas_fiscais_substituidas
IF servico = 'notas_fiscais_substituidas' THEN
  UPDATE "E_Nota".notas_fiscais_substituidas o
  SET contribuinte_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = o.contribuinte_origem_id AND o.contribuinte_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_substituidas nfs
  SET notas_substituidas_cloud_id = nf.id_gerado
  FROM "E_Nota".notas_fiscais nf
  WHERE nf.id = nfs.notas_substituidas_origem_id
    AND nfs.notas_substituidas_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;

  UPDATE "E_Nota".notas_fiscais_substituidas nfs
  SET notas_substitutas_cloud_id = nf.id_gerado
  FROM "E_Nota".notas_fiscais nf
  WHERE nf.id = nfs.notas_substitutas_origem_id
    AND nfs.notas_substitutas_cloud_id IS NULL
    AND nfs.id_gerado IS NULL;
END IF;

-- guias
IF servico = 'guias' THEN
  UPDATE "E_Nota".guias g
  SET contribuinte_cloud_id = p.id_gerado
  FROM "E_Nota".pessoas p
  WHERE p.id = g.contribuinte_cloud_id
    AND g.contribuinte_cloud_id IS NULL
    AND g.id_gerado IS NULL;

  UPDATE "E_Nota".guias g
  SET convenio_cloud_id = c.id_gerado
  FROM "E_Nota".convenios c
  WHERE c.id = g.convenio_cloud_id
    AND g.convenio_cloud_id IS NULL
    AND g.id_gerado IS NULL;

  UPDATE "E_Nota".guias g
  SET competencia_cloud_id = c.id_gerado
  FROM "E_Nota".competencias c
  WHERE c.id = g.competencia_cloud_id
    AND g.competencia_cloud_id IS NULL
    AND g.id_gerado IS NULL;

  UPDATE "E_Nota".guias n
  SET competencia_cloud_id = c.id_gerado
  FROM "E_Nota".competencias c
  WHERE n.competencia_descricao::date BETWEEN c.data_inicial AND c.data_final
    AND n.competencia_cloud_id IS NULL
    AND competencia_descricao IS NOT NULL
    AND n.id_gerado IS NULL;
END IF;

-- guias_notas
IF servico = 'guias_notas' THEN
  UPDATE "E_Nota".guias_notas g
  SET nota_cloud_id = gp.id_gerado
  FROM "E_Nota".notas_fiscais gp
  WHERE gp.id = g.nota_origem_id
    AND g.nota_cloud_id IS NULL
    AND g.id_gerado IS NULL;

  UPDATE "E_Nota".guias_notas n
  SET guia_cloud_id = gp.id_gerado
  FROM "E_Nota".guias gp
  WHERE n.guia_origem_id = gp.id
    AND n.guia_cloud_id IS NULL
    AND n.id_gerado IS NULL;
END IF;

RETURN true;
END;
$$ LANGUAGE plpgsql;
commit