

CREATE OR REPLACE FUNCTION "Protocolo".atualizar_dependencias(servico TEXT, sistema TEXT) RETURNS BOOLEAN AS $$
BEGIN

SET search_path TO "Protocolo";
SET search_path = "Protocolo";



IF servico = 'pessoas' THEN
  update "Protocolo".pessoas p
  set id_gerado = p2.id_gerado
  from "Protocolo".pessoas p2
  where p2.id_gerado is not null and p.id_gerado is null and p2.cpf_cnpj = p.cpf_cnpj and length(p2.cpf_cnpj) > 5;

IF servico = 'municipios' THEN
  UPDATE "Protocolo".municipios o
  SET estado_cloud_id = p.id_gerado
  FROM "Protocolo".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

IF servico = 'bairros' THEN
  UPDATE "Protocolo".bairros o
  SET municipio_cloud_id = p.id_gerado
  FROM "Protocolo".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;
END IF;

IF servico = 'logradouros' THEN
  UPDATE "Protocolo".logradouros o
  SET municipio_cloud_id = p.id_gerado
  FROM "Protocolo".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

UPDATE "Protocolo".logradouros p
SET id_gerado = p2.id_gerado
FROM (
  SELECT Protocolo, nome, municipio_cloud_id
  FROM "Protocolo".logradouros
  WHERE id_gerado IS NOT NULL
) p2
WHERE p.id_gerado IS NULL
  AND p2.municipio_cloud_id = p.municipio_cloud_id
  AND public.unaccent(lower(trim(p2.nome))) = public.unaccent(lower(trim(p.nome)));
END IF;


IF servico = 'pessoas_enderecos' THEN
  
  CREATE INDEX if not exists idx_bairros_municipio ON "Protocolo".bairros (municipio_cloud_id);
  CREATE INDEX if not exists idx_pessoas_enderecos_nulos ON "Protocolo".pessoas_enderecos (bairro_cloud_id, id_gerado, municipio_cloud_id);


  UPDATE "Protocolo".pessoas_enderecos o
  SET municipio_cloud_id = p.id_gerado
  FROM "Protocolo".municipios p
  WHERE p.id = o.municipio_origem_id AND o.municipio_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Protocolo".pessoas_enderecos o
  SET estado_cloud_id = p.id_gerado
  FROM "Protocolo".estados p
  WHERE p.id = o.estado_origem_id AND o.estado_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Protocolo".pessoas_enderecos o
  SET pessoa_cloud_id = p.id_gerado
  FROM "Protocolo".pessoas p
  WHERE p.id = o.pessoa_origem_id AND o.pessoa_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Protocolo".pessoas_enderecos o
  SET logradouro_cloud_id = p.id_gerado
  FROM "Protocolo".logradouros p
  WHERE p.id = o.logradouro_origem_id AND o.logradouro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Protocolo".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM "Protocolo".bairros p
  WHERE p.id = o.bairro_origem_id AND o.bairro_cloud_id IS NULL AND o.id_gerado IS NULL;

  UPDATE "Protocolo".pessoas_enderecos o
  SET bairro_cloud_id = p.id_gerado
  FROM (
      SELECT id_gerado, nome, municipio_cloud_id
      FROM "Protocolo".bairros
  ) p
  WHERE o.bairro_cloud_id IS NULL
    AND o.id_gerado IS NULL
    AND p.municipio_cloud_id = o.municipio_cloud_id
    AND public.unaccent(trim(p.nome)) ILIKE public.unaccent(trim(o.bairro_descricao));
END IF;

RETURN true;
END;
$$ LANGUAGE plpgsql;
commit