select id
,pessoa_origem_id
,pessoa_cloud_id
,tipo
,principal
,REGEXP_REPLACE(telefone, '[^0-9]', '', 'g') as telefone
,descricao
,observacao
,id_gerado
,mensagem
,atualizado from "E_Nota".pessoas_telefones where id_gerado is null