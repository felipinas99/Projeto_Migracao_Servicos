select * from "Livro_Eletronico".declaracoes_df_itens
where declaracao_cloud_id is not null
and lista_servico_cloud_id is not null
and documento_cloud_id is not null
and sequencia_cloud_id is not null
and atualizado is null
and id_gerado is null