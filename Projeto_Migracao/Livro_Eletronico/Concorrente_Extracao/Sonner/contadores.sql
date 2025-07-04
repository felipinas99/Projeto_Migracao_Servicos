select
	tp.contadorResponsavel_id as id
	, tp2.documento as inscricao
	, tpap2.crc as crc
from
	t_pessoa tp
left join t_papel tpap on
	tpap.id = tp.contadorResponsavel_id
left join t_pessoa tp2 on tp2.id = tpap.ator_id 
left join t_papel tpap2 on tpap2.ator_id = tp2.id
where
	tp.contadorResponsavel_id is not null and tpap2.perfil ='contador'
group by
	1,2,3