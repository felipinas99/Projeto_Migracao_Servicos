select
	te.id as id	
	, tg.id as guia_origem_id
	, te.documento_id as nota_origem_id
from
	t_encerramentodocumento te 
left join t_encerramento enc on
	enc.id = te.encerramento_id
left join t_guiaavulsa tg on
	tg.id = enc.guia_id
where enc.guia_id  is not null