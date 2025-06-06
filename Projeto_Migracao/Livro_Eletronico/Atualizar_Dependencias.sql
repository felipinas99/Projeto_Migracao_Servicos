

CREATE OR REPLACE FUNCTION "E_Nota".atualizar_dependencias(servico TEXT, sistema TEXT) RETURNS BOOLEAN AS $$
BEGIN

SET search_path TO sistema;

IF servico = 'pessoas_emails' THEN
  update "E_Nota".pessoas_emails o
  set pessoa_cloud_id = p.id_gerado
  from "E_Nota".pessoas p 
  where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;
end if;

RETURN true;
END;
$$ LANGUAGE plpgsql;
commit