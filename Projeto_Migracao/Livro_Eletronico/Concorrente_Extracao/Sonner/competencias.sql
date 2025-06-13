select
	row_number() over () as id
	, cast(row_number() over () as char) as descricao
	, tab.*
from
	(
with recursive meses as (
	select
		DATE('1980-01-01') as data_inicio
union all
	select
		DATE_ADD(data_inicio, interval 1 month)
	from
		meses
	where
		data_inicio < '2025-12-01'
)
	select
		cast(data_inicio as char)as data_inicial
		, cast(LAST_DAY(data_inicio)as char) as data_final
		, cast(DATE_ADD(LAST_DAY(data_inicio), interval 1 month)as char) as  data_vencimento
	from
		meses) as tab
