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

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".competencias (
    id INT PRIMARY KEY,
    descricao VARCHAR,
    data_inicial date,
    data_final date,
    data_vencimento VARCHAR,
    entidade_cloud_id VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".indexadores (
    id INT PRIMARY KEY,
    tipo VARCHAR,
    sigla VARCHAR,
    descricao VARCHAR,
    moeda_corrente VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".indexadores_valores (
    id INT PRIMARY KEY,
    indexador_origem_id int,
    indexador_cloud_id int,
    valor VARCHAR,
    data_hora_indexador VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".contribuintes (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    contador_origem_id INT,
    contador_cloud_id INT,
    tipo_origem_id INT,
    tipo_cloud_id INT,
    banco_origem_id INT,
    banco_cloud_id INT,
    lista_servico_origem_id INT,
    lista_servico_cloud_id INT,
    enquadramento VARCHAR,
    tipo_contribuinte VARCHAR,
    data_adesao_nota VARCHAR,
    tipo_pessoa VARCHAR,
    cpf_cnpj VARCHAR,
    optante_sn VARCHAR,
    escritura_dfp VARCHAR,
    escritura_dft VARCHAR,
    permite_deducao VARCHAR,
    declara_conjugada VARCHAR,
    descontado_prefeitura VARCHAR,
    permite_taxas_especiais VARCHAR,
    isento_taxa_expediente VARCHAR,
    possui_pendencias VARCHAR,
    permite_gerar_decl_por_documento VARCHAR,
    data_abertura VARCHAR,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".listas_servicos (
    id INT PRIMARY KEY,
    lista_servico_cloud_id VARCHAR,
    lista_servico_origem_id VARCHAR,
    aliquota VARCHAR,
    data_adesao VARCHAR,
    iss_devido_local_prest VARCHAR,
    indice_substituicao VARCHAR,
    permite_alterar_aliquota VARCHAR,
    indice_deducao VARCHAR,
    aliq_federal VARCHAR,
    aliq_estadual VARCHAR,
    aliq_municipal VARCHAR,
    versao_ibpt VARCHAR,
    entidade_cloud_id int,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".contribuintes_servicos (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    lista_servico_origem_id INT,
    lista_servico_cloud_id INT,
    cnae_origem_id INT,
    cnae_cloud_id INT,
    aliquota VARCHAR,
    servico_principal VARCHAR,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".contribuintes_mov_optante (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    data_inicio VARCHAR,
    data_efeito VARCHAR,
    descricao VARCHAR,
    motivo VARCHAR,
    orgao VARCHAR,
    optante_sn VARCHAR,
    mei VARCHAR,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "Livro_Eletronico".guias (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    competencia_origem_id INT,
    competencia_cloud_id INT,
    competencia_descricao date,
    numero_baixa VARCHAR,
    data_vencimento VARCHAR,
    data_referencia VARCHAR,
    vl_guia VARCHAR,
    vl_desconto VARCHAR,
    vl_juro VARCHAR,
    vl_multa VARCHAR,
    vl_correcao VARCHAR,
    vl_taxa_expediente VARCHAR,
    vl_imposto VARCHAR,
    situacao VARCHAR,
    tipo VARCHAR,
    nosso_numero VARCHAR,
    representacao_numerica VARCHAR,
    codigo_barras VARCHAR,
    nro_convenio VARCHAR,
    nro_banco VARCHAR,
    data_validade VARCHAR,
    vl_documento VARCHAR,
    data_emissao VARCHAR,
    data_vencimento_boleto VARCHAR,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);


CREATE TABLE IF NOT EXISTS "Livro_Eletronico".declarados (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    tipo_pessoa VARCHAR,
    pessoa_declarado_origem_id INT,
    pessoa_declarado_cloud_id INT,
    municipio_origem_id INT,
    municipio_cloud_id INT,
    cpf_cnpj VARCHAR,
    numero_documento VARCHAR,
    inscricao_municipal VARCHAR,
    inscricao_estadual VARCHAR,
    optante_sn VARCHAR,
    porte_empresa VARCHAR,
    nome VARCHAR,
    nome_fantasia VARCHAR,
    pais VARCHAR,
    municipio VARCHAR,
    bairro VARCHAR,
    endereco VARCHAR,
    numero VARCHAR,
    cep VARCHAR,
    complemento VARCHAR,
    email VARCHAR,
    telefone VARCHAR,
    site VARCHAR,
    celular VARCHAR,
    id_gerado jsonb,
    mensagem TEXT,
    atualizado VARCHAR
);


commit;