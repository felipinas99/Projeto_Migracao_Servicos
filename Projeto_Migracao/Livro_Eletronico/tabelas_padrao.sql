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

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".estados (
    id INT PRIMARY KEY,
    nome VARCHAR,
    sigla VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".municipios (
    id INT PRIMARY KEY,
    nome VARCHAR,
    uf VARCHAR,
    estado_origem_id int,
    estado_cloud_id int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".bairros (
    id INT PRIMARY KEY,
    municipio_origem_id int,
    municipio_cloud_id int,
    nome VARCHAR,
    padrao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".logradouros (
    id INT PRIMARY KEY,
    tipo_logradouro_descricao varchar,
    tipo_logradouro_origem_id int,
    tipo_logradouro_cloud_id int,
    municipio_origem_id int,
    municipio_cloud_id int,
    nome text,
    cep VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT EXISTS "Livro_Eletronico".pessoas_enderecos (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    estado_origem_id int,
    estado_cloud_id int,
    municipio_origem_id int,
    municipio_cloud_id int,
    bairro_origem_id int,
    bairro_cloud_id int,
    logradouro_origem_id int,
    logradouro_cloud_id int,
    condominio_origem_id int,
    condominio_cloud_id int,
    loteamento_origem_id int,
    loteamento_cloud_id int,
    distrito_origem_id int,
    distrito_cloud_id int,
    principal text,
    descricao text,
    tipo_endereco text,
    cep text,
    numero text,
    bloco text,
    complemento text,
    observacao text,
    apartamento text,
    bairro_descricao text,
    ordem int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


commit;