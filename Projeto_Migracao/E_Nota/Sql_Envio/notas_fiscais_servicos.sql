select * from "E_Nota".notas_fiscais_servicos 
where nota_fiscal_cloud_id is not null 
and lista_servico_entidade_cloud_id IS NOT NULL
and id_gerado is null