CREATE SCHEMA IF NOT EXISTS "E_Nota";
SET search_path TO "E_Nota";
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas (
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

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_perfis (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    imune VARCHAR,
    responsavel_tributario VARCHAR,
    permite_deducao_nf VARCHAR,
    permite_servico_descontado_nf VARCHAR,
    permite_rps_manual VARCHAR,
    permite_rps_eletronico VARCHAR,
    desconsiderar_taxa_diversa_rps VARCHAR,
    seq_nf INT,
    seq_rps_manual INT,
    seq_rps_eletronico INT,
    codigo_economico INT,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "E_Nota".estados (
    id INT PRIMARY KEY,
    nome VARCHAR,
    uf VARCHAR,
    pais_origem_id int,
    pais_cloud_id int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".municipios (
    id INT PRIMARY KEY,
    nome VARCHAR,
    uf VARCHAR,
    estado_origem_id int,
    estado_cloud_id int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_emails (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    descricao VARCHAR,
    principal VARCHAR,
    email VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_telefones (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    tipo VARCHAR,
    principal VARCHAR,
    telefone VARCHAR,
    descricao VARCHAR,
    observacao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".tipos_logradouros (
    id INT PRIMARY KEY,
    abreviatura VARCHAR,
    descricao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".logradouros (
    id INT PRIMARY KEY,
    tipo_logradouro_descricao varchar,
    tipo_logradouro_origem_id int,
    tipo_logradouro_cloud_id int,
    municipio_origem_id int,
    municipio_cloud_id int,
    nome VARCHAR,
    cep VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".bairros (
    id INT PRIMARY KEY,
    municipio_origem_id int,
    municipio_cloud_id int,
    nome VARCHAR,
    padrao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".bairros (
    id INT PRIMARY KEY,
    municipio_origem_id int,
    municipio_cloud_id int,
    nome VARCHAR,
    padrao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_enderecos (
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
    principal VARCHAR,
    descricao VARCHAR,
    cep VARCHAR,
    numero VARCHAR,
    bloco VARCHAR,
    complemento VARCHAR,
    observacao VARCHAR,
    apartamento VARCHAR,
    bairro_descricao VARCHAR,
    ordem int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT EXISTS "E_Nota".competencias (
    id INT PRIMARY KEY,
    descricao VARCHAR,
    exercicio int,
    data_inicial VARCHAR,
    data_final VARCHAR,
    data_vencimento VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".indexadores (
    id INT PRIMARY KEY,
    tipo_indexador VARCHAR,
    sigla VARCHAR,
    descricao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".movimentacoes_indexadores (
    id INT PRIMARY KEY,
    indexador_origem_id int,
    indexador_cloud_id int,
    valor_movimentacao VARCHAR,
    data_movimentacao VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".listas_servicos_entidades (
    id INT PRIMARY KEY,
    aliquota VARCHAR,
    data_adesao VARCHAR,
    iss_devido_local_prestacao VARCHAR,
    incide_substituicao_tributaria VARCHAR,
    permite_alterar_aliquota VARCHAR,
    incide_deducao VARCHAR,
    aliquota_federal decimal,
    aliquota_estadual decimal,
    aliquota_municipal decimal,
    data_inicio_vigencia VARCHAR,
    data_fim_vigencia VARCHAR,
    versao VARCHAR,
    descricao VARCHAR,
    codigo VARCHAR,
    listas_servicos_leis_origem_id INT,
    listas_servicos_leis_cloud_id INT,
    nivel decimal,
    desativado VARCHAR,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);


CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_listas_servicos_cnaes (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    codigo_cnae VARCHAR,
    lista_servico_entidade_origem_id int,
    lista_servico_entidade_cloud_id int,
    codigo_lista_servico_entidade varchar,
    aliquota VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_portes (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    motivo_origem_id int,
    motivo_cloud_id int,
    porte_empresa VARCHAR,
    data_efeito VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_simples_nacional (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    motivo_origem_id int,
    motivo_cloud_id int,
    orgao VARCHAR,
    optante VARCHAR,
    data_inicio VARCHAR,
    data_efeito VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".pessoas_atividades (
    id INT PRIMARY KEY,
    pessoa_origem_id int,
    pessoa_cloud_id int,
    data_movimentacao VARCHAR,
    tipo VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);

CREATE TABLE IF NOT EXISTS "E_Nota".notas_fiscais (
    id INT PRIMARY KEY,
    pessoa_origem_id INT,
    pessoa_cloud_id INT,
    nro_nota BIGINT,
    data_hora_fato_gerador VARCHAR,
    data_hora_emissao VARCHAR,
    nro_verificacao VARCHAR,
    situacao VARCHAR,
    competencias_descricao varchar,
    competencias_origem_id INT,
    competencias_cloud_id INT,
    optante_simples VARCHAR,
    natureza_operacao VARCHAR,
    situacao_tributaria VARCHAR,
    nro_processo_suspensao VARCHAR,
    nro_rps INT,
    series_rps_origem_id INT,
    series_rps_cloud_id INT,
    sigla_series_rps VARCHAR,
    data_hora_emissao_rps VARCHAR,
    nro_lote INT,
    nro_obra VARCHAR,
    nro_art VARCHAR,
    observacao_complementar VARCHAR,
    prestador_codigo INT,
    prestador_municipio VARCHAR,
    prestador_municipio_codigo INT,
    prestador_tipo_pessoa VARCHAR,
    prestador_inscricao VARCHAR,
    prestador_nome VARCHAR,
    prestador_nome_social_fantasia VARCHAR,
    prestador_inscricao_municipal VARCHAR,
    prestador_inscricao_estadual VARCHAR,
    prestador_cep VARCHAR,
    prestador_bairro VARCHAR,
    prestador_distrito_origem_id INT,
    prestador_distrito_cloud_id INT,
    prestador_distritos VARCHAR,
    prestador_logradouro VARCHAR,
    prestador_numero VARCHAR,
    prestador_complemento VARCHAR,
    prestador_estado VARCHAR,
    prestador_email VARCHAR,
    prestador_site VARCHAR,
    prestador_telefone VARCHAR,
    prestador_celular VARCHAR,
    prestador_fax VARCHAR,
    prestador_modalidade_iss VARCHAR,
    prestador_porte_empresa VARCHAR,
    prestador_imune VARCHAR,
    prestador_responsavel_tributario VARCHAR,
    tomador_origem_id INT,
    tomador_cloud_id INT,
    tomador_codigo INT,
    tomador_municipio VARCHAR,
    tomador_municipio_codigo INT,
    tomador_uf VARCHAR,
    tomador_tipo_pessoa VARCHAR,
    tomador_inscricao VARCHAR,
    tomador_nome VARCHAR,
    tomador_nome_social_fantasia VARCHAR,
    tomador_inscricao_municipal VARCHAR,
    tomador_inscricao_estadual VARCHAR,
    tomador_cep VARCHAR,
    tomador_bairro VARCHAR,
    tomador_logradouro VARCHAR,
    tomador_numero VARCHAR,
    tomador_complemento VARCHAR,
    tomador_email VARCHAR,
    tomador_site VARCHAR,
    tomador_telefone VARCHAR,
    tomador_celular VARCHAR,
    tomador_pais_origem_id INT,
    tomador_pais_cloud_id INT,
    tomador_optante_simples VARCHAR,
    tomador_porte_empresa VARCHAR,
    tomador_distrito VARCHAR,
    intermediario_origem_id INT,
    intermediario_cloud_id INT,
    intermediario_codigo INT,
    intermediario_inscricao VARCHAR,
    intermediario_nome VARCHAR,
    intermediario_inscricao_municipal VARCHAR,
    vl_pis DECIMAL,
    vl_cofins DECIMAL,
    vl_inss DECIMAL,
    vl_ir DECIMAL,
    vl_csll DECIMAL,
    vl_outras_retencoes DECIMAL,
    vl_aliquota_pis DECIMAL,
    vl_aliquota_cofins DECIMAL,
    vl_aliquota_inss DECIMAL,
    vl_aliquota_ir DECIMAL,
    vl_aliquota_csll DECIMAL,
    vl_aliquota_outras DECIMAL,
    pais_servico_origem_id INT,
    pais_servico_cloud_id INT,
    municipio_servico_origem_id INT,
    municipio_servico_cloud_id INT,
    servico_descontado_prefeitura VARCHAR,
    servico_prestado_pais VARCHAR,
    vl_total_servicos DECIMAL,
    vl_total_descontos_condicionados DECIMAL,
    vl_total_descontos_incondicionados DECIMAL,
    vl_total_deducoes DECIMAL,
    vl_total_liquido DECIMAL,
    vl_total_base_calculo DECIMAL,
    vl_total_iss DECIMAL,
    vl_total_iss_outros DECIMAL,
    aliquota_ibpt_federal DECIMAL,
    aliquota_ibpt_estadual DECIMAL,
    aliquota_ibpt_municipal DECIMAL,
    vl_tributo_federal DECIMAL,
    vl_tributo_estadual DECIMAL,
    vl_tributo_municipal DECIMAL,
    protocolo_rps VARCHAR,
    responsavel_retencao VARCHAR,
    versao_rps VARCHAR,
    rps_fora_do_prazo VARCHAR,
    rps_data_limite VARCHAR,
    tipo_certificado VARCHAR,
    utiliza_aliquota_municipal VARCHAR,
    integracao_disponivel VARCHAR,
    pis_pasep VARCHAR,
    data_emissao_pis_pasep VARCHAR,
    situacao_guia VARCHAR,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "E_Nota".notas_fiscais_servicos (
    id INT PRIMARY KEY,
    nota_fiscal_origem_id INT,
    nota_fiscal_cloud_id INT,
    cnae_origem_id INT,
    cnae_cloud_id INT,
    descricao_cnae VARCHAR,
    lista_servico_entidade_origem_id INT,
    lista_servico_entidade_cloud_id INT,
    descricao_lista_servico_entidade VARCHAR,
    descontado_prefeitura varchar,
    aliquota DECIMAL,
    prestado_pais VARCHAR,
    pais_origem_id INT,
    pais_cloud_id INT,
    municipio_origem_id INT,
    municipio_cloud_id INT,
    discriminacao VARCHAR,
    vl_servico DECIMAL,
    quantidade DECIMAL,
    vl_total_servico DECIMAL,
    vl_desconto_condicionado DECIMAL,
    vl_desconto_incondicionado DECIMAL,
    vl_deducao DECIMAL,
    vl_base_calculo DECIMAL,
    vl_iss DECIMAL,
    vl_iss_outros DECIMAL,
    aliquota_ibpt DECIMAL,
    aliquota_ibpt_federal DECIMAL,
    aliquota_ibpt_estadual DECIMAL,
    aliquota_ibpt_municipal DECIMAL,
    vl_tributo_federal DECIMAL,
    vl_tributo_estadual DECIMAL,
    vl_tributo_municipal DECIMAL,
    fonte_ibpt VARCHAR,
    codigo_tabela VARCHAR,
    tabela_padrao VARCHAR,
    anexo VARCHAR,
    faixa VARCHAR,
    faturamento_inicial DECIMAL,
    faturamento_final DECIMAL,
    vl_rbt12 DECIMAL,
    rbt12_mes_anterior DECIMAL,
    vl_soma_rbt12_meses DECIMAL,
    vl_soma_folha_12_meses DECIMAL,
    vl_folha_pgto_12 DECIMAL,
    perc_gasto_folha DECIMAL,
    descricao_receita_bruta VARCHAR,
    descricao_beneficio_fiscal VARCHAR,
    tipo_beneficio_fiscal VARCHAR,
    aplicacao_incentivo VARCHAR,
    percentual_reducao DECIMAL,
    aliquota_original DECIMAL,
    vl_base_calculo_original DECIMAL,
    vl_iss_original DECIMAL,
    municipio_incidencia_origem_id INT,
    municipio_incidencia_cloud_id INT,
    script_origem_id INT,
    script_cloud_id INT,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "E_Nota".notas_fiscais_cancelamento (
    id INT PRIMARY KEY,
    contribuinte_origem_id INT,
    contribuinte_cloud_id INT,
    nota_fiscal_origem_id INT,
    nota_fiscal_cloud_id INT,
    processo VARCHAR,
    motivo VARCHAR,
    data_hora_cancelamento VARCHAR,
    nro_prtocolo VARCHAR,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT EXISTS "E_Nota".notas_fiscais_substituidas (
    id INT PRIMARY KEY,
    contribuinte_origem_id INT,
    contribuinte_cloud_id INT,
    notas_substitutas_origem_id INT,
    notas_substitutas_cloud_id INT,
    notas_substituidas_origem_id INT,
    notas_substituidas_cloud_id INT,
    nro_protocolo TEXT,
    motivo_substituicao TEXT,
    data_hora_substituicao TEXT,
    id_gerado INT,
    mensagem TEXT,
    atualizado VARCHAR
);

CREATE TABLE IF NOT exists "E_Nota".guias (
    id INT PRIMARY KEY,
    contribuinte_origem_id int,
    contribuinte_cloud_id int,
    convenio_origem_id int,
    convenio_cloud_id int,
    competencia_origem_id int,
    competencia_cloud_id int,
    guia_principal_origem_id int,
    guia_principal_cloud_id int,
    data_hora_geracao varchar,
    data_hora_integracao_geracao varchar,
    data_hora_integracao_alteracao varchar,
    data_hora_integracao_cancelamento varchar,
    data_vencimento varchar,
    data_documento varchar,
    data_vencimento_documento varchar,
    data_validade varchar,
    nro_parcela bigint,
    nro_baixa INTEGER,
    tipo_guia VARCHAR,
    tipo_geracao VARCHAR,
    sistema_origem VARCHAR,
    situacao VARCHAR,
    quantidade_notas INTEGER,
    vl_servico NUMERIC,
    vl_tributo NUMERIC,
    vl_base_calculo NUMERIC,
    vl_taxa_expediente NUMERIC,
    vl_saldo_utilizado NUMERIC,
    vl_guia NUMERIC,
    vl_documento NUMERIC,
    nosso_numero VARCHAR,
    codigo_barras VARCHAR,
    representacao_numerica VARCHAR,
    motivo_cancelamento VARCHAR,
    data_hora_cancelamento varchar,
    usuario_cancelamento VARCHAR,
    situacao_registro_bancario VARCHAR,
    mensagem_registro_bancario VARCHAR,
    tipo_operacao_registro_bancario VARCHAR,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT exists "E_Nota".guias (
    id INT PRIMARY KEY,
    guia_origem_id int,
    guia_cloud_id int,
    nota_origem_id int,
    nota_cloud_id int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


CREATE TABLE IF NOT exists "E_Nota".guias_notas (
    id INT PRIMARY KEY,
    guia_origem_id int,
    guia_cloud_id int,
    nota_origem_id int,
    nota_cloud_id int,
    id_gerado int,
    mensagem text,
    atualizado varchar
);


update "E_Nota".pessoas_emails o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;

update "E_Nota".pessoas_telefones o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;

update "E_Nota".municipios o
set estado_cloud_id = p.id_gerado
from "E_Nota".estados p 
where p.id  = o.estado_origem_id and o.estado_cloud_id is null and o.id_gerado is null;

update "E_Nota".logradouros o
set municipio_cloud_id = p.id_gerado
from "E_Nota".municipios p 
where p.id  = o.municipio_origem_id and o.municipio_cloud_id is null and o.id_gerado is null;
update "E_Nota".logradouros o
set tipo_logradouro_cloud_id = p.id_gerado
from "E_Nota".tipos_logradouros p 
where p.id  = o.tipo_logradouro_origem_id and o.tipo_logradouro_cloud_id is null and o.id_gerado is null;
update "E_Nota".logradouros o
set tipo_logradouro_cloud_id = p.id_gerado
from "E_Nota".tipos_logradouros p 
where p.descricao  ilike o.tipo_logradouro_descricao and o.tipo_logradouro_cloud_id is null and o.id_gerado is null;

update
	"E_Nota".logradouros p
set
	id_gerado = p2.id_gerado
from
	"E_Nota".logradouros p2
where
	p2.id_gerado is not null
	and p.id_gerado is null
	and trim(p2.nome) ilike trim(p.nome)
	and p2.municipio_cloud_id  = p.municipio_cloud_id;


update "E_Nota".bairros o
set municipio_cloud_id = p.id_gerado
from "E_Nota".municipios p 
where p.id  = o.municipio_origem_id and o.municipio_cloud_id is null and o.id_gerado is null;


update "E_Nota".pessoas_enderecos o
set municipio_cloud_id = p.id_gerado
from "E_Nota".municipios p 
where p.id  = o.municipio_origem_id and o.municipio_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_enderecos o
set estado_cloud_id = p.id_gerado
from "E_Nota".estados p 
where p.id  = o.estado_origem_id and o.estado_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_enderecos o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_enderecos o
set logradouro_cloud_id = p.id_gerado
from "E_Nota".logradouros p 
where p.id  = o.logradouro_origem_id and o.logradouro_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_enderecos o
set bairro_cloud_id = p.id_gerado
from "E_Nota".bairros p 
where p.id  = o.bairro_origem_id and o.bairro_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_enderecos o
set bairro_cloud_id = p.id_gerado
from "E_Nota".bairros p 
where unaccent(trim(p.nome))  ilike unaccent(trim(o.bairro_descricao))
and p.municipio_cloud_id  = o.municipio_cloud_id and o.bairro_cloud_id is null and o.id_gerado is null;

update "E_Nota".pessoas_listas_servicos_cnaes o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;
update "E_Nota".pessoas_listas_servicos_cnaes o
set lista_servico_entidade_cloud_id = p.id_gerado
from "E_Nota".listas_servicos_entidades p 
where p.id  = o.lista_servico_entidade_origem_id and o.lista_servico_entidade_cloud_id is null and o.id_gerado is null;

update "E_Nota".pessoas_listas_servicos_cnaes o
set codigo_lista_servico_entidade = p.codigo
from "E_Nota".listas_servicos_entidades p 
where p.id_gerado  = o.lista_servico_entidade_cloud_id and o.lista_servico_entidade_cloud_id is not null and o.id_gerado is null;


update "E_Nota".pessoas_portes o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;


update "E_Nota".pessoas_simples_nacional o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;

update "E_Nota".pessoas_atividades o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;



-- Atualiza pessoa_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p
where p.id = n.pessoa_origem_id and n.pessoa_cloud_id is null and n.id_gerado is null;

-- Atualiza competencias_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set competencias_cloud_id = c.id_gerado
from "E_Nota".competencias c
where c.id = n.competencias_origem_id and n.competencias_cloud_id is null and competencias_origem_id is not null and n.id_gerado is null;

update "E_Nota".notas_fiscais n
set competencias_cloud_id = c.id_gerado
from "E_Nota".competencias c
where n.competencias_descricao  BETWEEN c.data_inicial AND c.data_final and n.competencias_cloud_id is null and competencias_descricao is not null  and n.id_gerado is null;


-- Atualiza series_rps_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set series_rps_cloud_id = s.id_gerado
from "E_Nota".series_rps s
where s.id = n.series_rps_origem_id and n.series_rps_cloud_id is null and n.id_gerado is null;

-- Atualiza prestador_distrito_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set prestador_distrito_cloud_id = d.id_gerado
from "E_Nota".distritos d
where d.id = n.prestador_distrito_origem_id and n.prestador_distrito_cloud_id is null and n.id_gerado is null;

-- Atualiza tomador_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set tomador_cloud_id = p.id_gerado
from "E_Nota".pessoas p
where p.id = n.tomador_origem_id and n.tomador_cloud_id is null and n.id_gerado is null;

-- Atualiza tomador_pais_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set tomador_pais_cloud_id = p.id_gerado
from "E_Nota".paises p
where p.id = n.tomador_pais_origem_id and n.tomador_pais_cloud_id is null and n.id_gerado is null;

-- Atualiza intermediario_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set intermediario_cloud_id = p.id_gerado
from "E_Nota".pessoas p
where p.id = n.intermediario_origem_id and n.intermediario_cloud_id is null and n.id_gerado is null;

-- Atualiza pais_servico_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set pais_servico_cloud_id = p.id_gerado
from "E_Nota".paises p
where p.id = n.pais_servico_origem_id and n.pais_servico_cloud_id is null and n.id_gerado is null;

-- Atualiza municipio_servico_cloud_id em notas_fiscais
update "E_Nota".notas_fiscais n
set municipio_servico_cloud_id = m.id_gerado
from "E_Nota".municipios m
where m.id = n.municipio_servico_origem_id and n.municipio_servico_cloud_id is null and n.id_gerado is null;

-- Atualiza nota_fiscal_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET nota_fiscal_cloud_id = nf.id_gerado
FROM "E_Nota".notas_fiscais nf
WHERE nf.id = nfs.nota_fiscal_origem_id
  AND nfs.nota_fiscal_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza cnaes_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET cnae_cloud_id = c.id_gerado
FROM "E_Nota".cnaes c
WHERE c.id = nfs.cnae_origem_id
  AND nfs.cnae_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza listas_servicos_entidades_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET lista_servico_entidade_cloud_id = lse.id_gerado
FROM "E_Nota".listas_servicos_entidades lse
WHERE lse.id = nfs.lista_servico_entidade_origem_id
  AND nfs.lista_servico_entidade_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza paises_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET pais_cloud_id = p.id_gerado
FROM "E_Nota".paises p
WHERE p.id = nfs.pais_origem_id
  AND nfs.pais_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza municipios_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET municipio_cloud_id = m.id_gerado
FROM "E_Nota".municipios m
WHERE m.id = nfs.municipio_origem_id
  AND nfs.municipio_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza municipios_incidencia_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET municipio_incidencia_cloud_id = m.id_gerado
FROM "E_Nota".municipios m
WHERE m.id = nfs.municipio_incidencia_origem_id
  AND nfs.municipio_incidencia_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;

-- Atualiza script_cloud_id em notas_fiscais_servicos
UPDATE "E_Nota".notas_fiscais_servicos nfs
SET script_cloud_id = s.id_gerado
FROM "E_Nota".scripts s
WHERE s.id = nfs.script_origem_id
  AND nfs.script_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;


update "E_Nota".notas_fiscais_cancelamento o
set contribuinte_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.contribuinte_origem_id and o.contribuinte_cloud_id is null and o.id_gerado is null;

UPDATE "E_Nota".notas_fiscais_cancelamento nfs
SET nota_fiscal_cloud_id = nf.id_gerado
FROM "E_Nota".notas_fiscais nf
WHERE nf.id = nfs.nota_fiscal_origem_id
  AND nfs.nota_fiscal_cloud_id IS NULL
  AND nfs.id_gerado IS NULL;


update "E_Nota".notas_fiscais_substituidas o
set contribuinte_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.contribuinte_origem_id and o.contribuinte_cloud_id is null and o.id_gerado is null;

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


-- Atualiza contribuinte_cloud_id em guias
UPDATE "E_Nota".guias g
SET contribuinte_cloud_id = p.id_gerado
FROM "E_Nota".pessoas p
WHERE p.id = g.contribuinte_cloud_id
  AND g.contribuinte_cloud_id IS NULL
  AND g.id_gerado IS NULL;

-- Atualiza convenio_cloud_id em guias
UPDATE "E_Nota".guias g
SET convenio_cloud_id = c.id_gerado
FROM "E_Nota".convenios c
WHERE c.id = g.convenio_cloud_id
  AND g.convenio_cloud_id IS NULL
  AND g.id_gerado IS NULL;

-- Atualiza competencia_cloud_id em guias
UPDATE "E_Nota".guias g
SET competencia_cloud_id = c.id_gerado
FROM "E_Nota".competencias c
WHERE c.id = g.competencia_cloud_id
  AND g.competencia_cloud_id IS NULL
  AND g.id_gerado IS NULL;


update "E_Nota".guias n
set competencia_cloud_id = c.id_gerado
from "E_Nota".competencias c
where n.competencia_descricao::date  BETWEEN c.data_inicial AND c.data_final and n.competencia_cloud_id is null and competencia_descricao is not null  and n.id_gerado is null;



UPDATE "E_Nota".guias_notas g
SET nota_cloud_id = gp.id_gerado
FROM "E_Nota".notas_fiscais gp
WHERE gp.id = g.nota_origem_id
  AND g.nota_cloud_id IS NULL
  AND g.id_gerado IS NULL


update "E_Nota".guias_notas n
set guia_cloud_id = gp.id_gerado
from "E_Nota".guias gp
where n.guia_origem_id  = gp.id
and n.guia_cloud_id is null 
and n.id_gerado  is null


update "E_Nota".pessoas_perfis o
set pessoa_cloud_id = p.id_gerado
from "E_Nota".pessoas p 
where p.id  = o.pessoa_origem_id and o.pessoa_cloud_id is null and o.id_gerado is null;

commit;