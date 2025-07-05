select
	id
	, 'Obrigatório informar competencias_cloud_id' as mensagem
	, 'revisar extracao ou atualizacao de dependencias' as conselho
from
	"E_Nota".notas_fiscais nf
where
	nf.competencias_cloud_id is null