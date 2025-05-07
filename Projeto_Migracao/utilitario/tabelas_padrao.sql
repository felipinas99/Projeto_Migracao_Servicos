CREATE SCHEMA IF NOT EXISTS motor;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE OR REPLACE VIEW lotes_pendentes_envio AS
SELECT id, tipo_registro, lote_envio
FROM protocolo.controle_lotes
WHERE status_envio in ('NAO_ENVIADO') and lote_id is null;

CREATE OR REPLACE VIEW lotes_pendentes_processamento AS
SELECT id, tipo_registro, lote_id
FROM protocolo.controle_lotes
WHERE status_envio in ('ENVIADO', 'PROCESSANDO') and lote_id is not null;

CREATE OR REPLACE VIEW lotes_pendentes_resgate AS
SELECT id, tipo_registro, lote_recebido
FROM protocolo.controle_lotes
WHERE status_envio in ('PROCESSADO') and lote_id is not null and ids_atualizados = false;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_lote_envio') THEN
        CREATE TYPE motor.status_lote_envio AS ENUM ('NAO_ENVIADO', 'ENVIADO', 'PROCESSANDO', 'PROCESSADO', 'ERRO');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'metodo') THEN
        CREATE TYPE motor.metodo AS ENUM ('POST', 'GET', 'PUT', 'PATCH', 'DELETE');
    END IF;
END $$;


CREATE TABLE if not exists motor.controle_lotes (
    id SERIAL PRIMARY KEY,  
    tipo_registro VARCHAR,  
    metodo metodo,
    lote_envio JSONB,
    status_envio tipo_pessoa_enum,
    lote_id as varchar,
    lote_recebido JSONB ,
    ids_atualizados BOOLEAN DEFAULT false
);

commit;