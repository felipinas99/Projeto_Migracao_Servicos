select * from "E_Nota".notas_fiscais 
where competencias_cloud_id is not null 
and nro_verificacao is not null
and atualizado is null 
and id_gerado is null