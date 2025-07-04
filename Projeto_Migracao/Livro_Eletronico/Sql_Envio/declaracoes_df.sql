select * from "Livro_Eletronico".declaracoes_df 
where declaracao_cloud_id is not null
and atualizado is null
and documento_cloud_id is not null
and data_emissao is not null
and id_gerado is null