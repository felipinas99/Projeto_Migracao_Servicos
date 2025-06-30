CREATE SCHEMA IF NOT EXISTS motor;
SET search_path TO motor;
CREATE EXTENSION IF NOT EXISTS unaccent;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_lote_envio') THEN
        CREATE TYPE motor.status_lote_envio AS ENUM ('NAO_ENVIADO', 'ENVIADO', 'PROCESSANDO', 'PROCESSADO','AGUARDANDO_EXECUCAO', 'ERRO', 'DESCONHECIDO');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'metodo') THEN
        CREATE TYPE motor.metodo AS ENUM ('POST', 'GET', 'PUT', 'PATCH', 'DELETE');
    END IF;
END $$;


CREATE TABLE if not exists controle_lotes (
    id SERIAL PRIMARY KEY,  
    sistema VARCHAR,  
    tipo_registro VARCHAR,  
    servico VARCHAR,  
    metodo metodo,
    lote_envio JSONB,
    status_envio status_lote_envio DEFAULT 'NAO_ENVIADO',
    lote_envio_retorno JSONB,
    lote_id  varchar,
    lote_recebido JSONB,
    ids_atualizados BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS parametros (
    id SERIAL PRIMARY KEY,  
    tipo_parametro VARCHAR UNIQUE,
    valor VARCHAR
);

INSERT INTO motor.parametros (tipo_parametro, valor) VALUES
    ('Token',        '1'),
    ('Sistema',      'Livro_Eletronico'),
    ('Concorrente',  'Sonner'),
    ('Url_Base',     'https://livroeletronico.betha.cloud/livro-eletronico2/service-layer-livro/api/'),
    ('Url_Lote',     'https://livroeletronico.betha.cloud/livro-eletronico2/service-layer-livro/api/declaracoes/'),
    ('Entidade',     '1');



CREATE OR REPLACE VIEW lotes_pendentes_envio AS
SELECT id, sistema, metodo, tipo_registro,  servico, lote_envio
FROM controle_lotes
WHERE status_envio in ('NAO_ENVIADO') and lote_id is null;

CREATE OR REPLACE VIEW lotes_pendentes_processamento AS
SELECT id, sistema, status_envio, tipo_registro, lote_id
FROM controle_lotes
WHERE status_envio in ('ENVIADO', 'PROCESSANDO', 'AGUARDANDO_EXECUCAO','DESCONHECIDO') and lote_id is not null;

CREATE OR REPLACE VIEW lotes_pendentes_resgate AS
SELECT id, sistema, metodo, tipo_registro, lote_recebido
FROM controle_lotes
WHERE status_envio in ('PROCESSADO') and lote_id is not null and ids_atualizados = false and lote_recebido is not null;

commit;