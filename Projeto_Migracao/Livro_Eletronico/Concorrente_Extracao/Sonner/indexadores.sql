select id 
,nome as descricao 
, cast(nome as char(3)) as sigla
,'I' as tipo
from t_indice ti 