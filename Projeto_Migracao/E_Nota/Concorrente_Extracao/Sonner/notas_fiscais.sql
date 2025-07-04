select
	tn.id as id
	, a.vl_inss as vl_inss
	, a.vl_ir as vl_ir
	, a.vl_pis as vl_pis
	, a.vl_cofins as vl_cofins
	, a.vl_csll as vl_csll
	, a.vl_total_base_calculo
	,  valorTotal - a.vl_inss - a.vl_ir - a.vl_pis - a.vl_csll - a.vl_total_iss   as vl_total_liquido
	, a.vl_total_descontos_condicionados
	, a.vl_total_descontos_incondicionados
	, a.vl_total_deducoes
	, a.vl_outras_retencoes
	, a.vl_total_servicos
	, a.vl_total_iss
	, a.vl_total_iss_outros
	, a.vl_tributo_municipal
	, prestador_id as pessoa_origem_id
	, numero as nro_nota
	, CAST(correlacao AS UNSIGNED)  as nro_rps
	, td.emissao as data_hora_fato_gerador
	, td.emissao as data_hora_emissao
	, upper(CONCAT(SUBSTRING(td.senha, 1, 4), SUBSTRING(td.senha, 5, 4))) as nro_verificacao
	, case
		when td.dataCancelamento is not null then 'CANCELADA'
		else 'NORMAL'
	end as situacao
	, dataPrestacao as competencias_descricao
	, case
		when tipoRegimePrestador = 'SIMPLES' then 'SIM'
		else 'NAO'
	end as optante_simples
	, 'TRIBUTACAO_MUNICIPIO' as natureza_operacao
	, 'NORMAL' as situacao_tributaria
	, cast(obs as char(500))as observacao_complementar
	, prestador_id as prestador_codigo
	, municipioPrestador as prestador_municipio
	, case
		when length(documento) < 12 then 'FISICA'
		when length(documento) < 15 then 'JURIDICA'
		when length(documento) > 14 then 'JURIDICA'
		else 'JURIDICA'
	end as prestador_tipo_pessoa
	, docPrestador as prestador_inscricao
	, cast(nomePrestador as char(155)) as prestador_nome
	, cast(REGEXP_REPLACE(tp.inscMun, '[^0-9]', '') as char(15)) as prestador_inscricao_municipal
	, cast(REGEXP_REPLACE(tn.inscEstPrestador, '[^0-9]', '') as char(15)) as prestador_inscricao_estadual
	, cast(REGEXP_REPLACE(cepPrestador, '[^0-9]', '') as char(8)) as prestador_cep
	, cast(bairroPrestador as char(60)) as prestador_bairro
	, enderecoPrestador as prestador_logradouro
	, cast(numeroPrestador as char(10)) as prestador_numero
	, cast(complementoPrestador as char(100)) as prestador_complemento
	, estadoPrestador as prestador_estado
	, cast(email as char(80)) as prestador_email
	, cast(REGEXP_REPLACE(telefonePrestador, '[^0-9]', '') as char(8)) as prestador_telefone
	, nomeFantasiaPrestador as prestador_nome_social_fantasia
	, municipioTomador as tomador_municipio
	, cast(REGEXP_REPLACE(estadoTomador, '[^0-9]', '') as char(2)) as tomador_uf
	, docTomador  as tomador_inscricao
	, cast(nomeTomador as char(155)) as tomador_nome
	, cast(bairroTomador as char(60)) as tomador_bairro
	, nomeFantasiaTomador as tomador_nome_social_fantasia
	, cast(REGEXP_REPLACE(tn.inscMunTomador, '[^0-9]', '') as char(15))  as tomador_inscricao_municipal
	, cast(REGEXP_REPLACE(tn.inscEstTomador, '[^0-9]', '') as char(15)) as tomador_inscricao_estadual
	,cast(REGEXP_REPLACE(cepTomador, '[^0-9]', '') as char(8)) as tomador_cep
	, enderecoTomador as tomador_logradouro
	, cast(numeroTomador as char(10)) as tomador_numero
	, cast(complementoTomador as char(100)) as tomador_complemento
	, cast(emailTomador as char(80)) as tomador_email
	, cast(REGEXP_REPLACE(telefoneTomador, '[^0-9]', '') as char(8)) as tomador_telefone
	, case when municipioIncidencia_id is not null then municipioIncidencia_id else tn.municipio_id end as municipio_servico_origem_id
	, case
		when tr.tipo = 'Isento' then 'SIM'
		when tr.tipo = 'webIssIsento' then 'SIM'
		else 'NAO'
	end as prestador_imune
	, case 
	  when tr.tipo  = 'Faturamento' then 'HOMOLOGADO' 
	  when tr.tipo  = 'Estimativa' then 'ESTIMADO' 
	  when tr.tipo  = 'Simples' then 'HOMOLOGADO' 
	  when tr.tipo  = 'FixoAnual' then 'FIXO' 
	  when tr.tipo  = 'SociedadeProfissional' then 'FIXO' 
	  when tr.tipo  = 'NaoIncide' then 'NAO_ENQUADRADO' 
	  end as prestador_modalidade_iss
from
	t_notafiscal tn
left join t_documento td on
	td.id = tn.id
left join t_pessoa tp on
	tp.id = prestador_id
left join t_regimeiss tr on
	tr.id = tp.regimeISS_id
left join lateral (
	select
	case when descontoCondicional is null then 0 else descontoCondicional end as vl_total_descontos_condicionados
	, case when descontoIncondicional is null then 0 else descontoIncondicional end as vl_total_descontos_incondicionados
	, case when outrasDeducoes is null then 0 else outrasDeducoes end as vl_total_deducoes
	, case when outrasRetencoes is null then 0 else outrasRetencoes end as vl_outras_retencoes
	, case when valorTotal is null then 0 else valorTotal end vl_total_servicos
	, case when valorTotal is null then 0 else valorTotal end vl_total_base_calculo
	, case when valorImposto is null then 0 else valorImposto end as vl_total_iss
	, 0 as vl_total_iss_outros
	, case when valorImposto is null then 0 else valorImposto end as vl_tributo_municipal
	, case when retencaoINSS is null then 0 else retencaoINSS end as vl_inss
	, case when retencaoIRRF is null then 0 else retencaoIRRF end as vl_ir
	, case when retencaoPIS is null then 0 else retencaoPIS end as vl_pis
	, case when retencaoCOFINS is null then 0 else retencaoCOFINS end as vl_cofins
	, case when retencaoCSLL is null then 0 else retencaoCSLL end as vl_csll
) a on
	true