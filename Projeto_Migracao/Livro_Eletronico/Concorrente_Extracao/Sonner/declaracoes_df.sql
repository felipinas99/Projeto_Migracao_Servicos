select
	te.id
	, encerramento_id as declaracao_origem_id
	, te.idDocumento as documento_origem_id
	, te.idDocumento as documento_cloud_id
	, td.contribuinte_id as contribuinte_origem_id
	, serie as serie_descricao
	, te.numero as df_inicial
	, te.numero as df_final
	, cast(td.emissao as date) as data_emissao
	, case
		when cancelada = '0' then 'N'
		when cancelada = '1' then 'C'
	end as status
	, 'N' as tipo
	, 1 as natureza_operacao
	, case
		when retida = 1 then 'R'
		else 'N'
	end as situacao_tributaria
	, 'N' as descontado_prefeitura
	, case
		when cancelada = 0 then COALESCE(tn.valorImposto,0)
		else 0
	end as vl_imposto
	-- , valorBaseCalculo
	-- , tn.tipoTributacao_id
	, retencaoINSS as vl_inss
	, retencaoIRRF as vl_ir
	, retencaoPIS as vl_pis_pasep
	, retencaoCOFINS as vl_cofins
	, retencaoCSLL as vl_csll
	, case
		when outrasDeducoes is null then 0
		else outrasDeducoes
	end as vl_deducao
	, case
		when outrasRetencoes is null then 0
		else outrasRetencoes
	end as vl_outras_retencoes
	, case
		when valorTotal is null then 0
		else valorTotal
	end vl_servico
	, case
		when valorTotal is null then 0
		else valorTotal
	end vl_base_calculo
	, case
		when valorTotal is null then 0
		else valorTotal
	end vl_documento
	, valorTotal - tn.valorImposto as vl_liquido
	, case
		when tn.tipoRegimePrestador = 'Simples' then 'S'
		else 'N'
	end as optante_sn
from
	t_encerramentomemoria te
left join t_documento td on
	td.id = te.idDocumento
left join t_encerramento ter on
	ter.id = te.encerramento_id
left join t_notafiscal tn on
	tn.id = te.idDocumento