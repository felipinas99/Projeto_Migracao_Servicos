select
	s.id
	, dataSolicitacao
	, case
		when s.situacao = 'aprovada' then 'AUTORIZADO'
		when s.situacao = 'indeferida' then 'DESAUTORIZADO'
		when s.situacao = 'pendente' then 'DESAUTORIZADO'
	end as status
	, dataDeferimento
	, td.dataValidade
	, td.emissao
	, s.dataDeferimento
	, dataIndeferimento
	, motivoIndeferimento
	, indeferidor_id
	, aprovador_id
	, motivoDeferimento
from
		t_solicitacao s
left join t_pessoa tp on
		tp.id = s.contribuinte_id
left join t_documento td on
	td.id = s.documento_id
where
		tp.prestador = 1
	and tipo = 'ANFE'
		and s.id = 1611354