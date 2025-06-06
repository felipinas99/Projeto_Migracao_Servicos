CREATE SCHEMA IF NOT EXISTS "Livro_Eletronico";
SET search_path TO "Livro_Eletronico";
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".pessoas (
    id INT PRIMARY KEY,
    codigo VARCHAR,
    tipo_pessoa VARCHAR,
    inscricao VARCHAR,
    inscricao_municipal VARCHAR,
    inscricao_estadual VARCHAR,
    nome VARCHAR,
    nome_social_fantasia VARCHAR,
    possui_inscricao_estadual VARCHAR,
    orgao_registro VARCHAR,
    data_registro VARCHAR,
    nro_registro VARCHAR,
    modalidade_iss VARCHAR,
    situacao_economico VARCHAR,
    funcao_responsavel VARCHAR,
    site VARCHAR,
    autorizacao_emissao_nf VARCHAR,
    motivo VARCHAR,
    pis_pasep VARCHAR,
    data_emissao_pis_pasep VARCHAR,
    id_pessoas_perfis INT,
    id_natureza_juridica INT,
    id_qualificacao INT,
    id_responsavel INT,
    perfil VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


commit;