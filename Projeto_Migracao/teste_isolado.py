from utilitario.Funcoes import *

banco_envio_parametros={"usuario" : 'postgres',"senha" : 'admin',"banco_dados" : 'Migracao',"host" : 'localhost',"porta" : '5432'}
cursor = iniciarCursorPostgresql(banco_envio_parametros["host"], banco_envio_parametros["banco_dados"], banco_envio_parametros["porta"], banco_envio_parametros["usuario"], banco_envio_parametros["senha"])


sql = "SELECT * FROM contribuintes"

def colunas_sql(cursor, sql):
    cursor.execute(sql)
    colunas = [desc[0] for desc in cursor.description]
    placeholders = ', '.join(['?'] * len(colunas))  # pyodbc usa '?'
    return placeholders, colunas

def montar_insercao(cursor,sql):

    placeholders, colunas = colunas_sql(cursor, sql)
    dados = cursor.fetchall()

    colunas_update = [f"{col} = EXCLUDED.{col}" for col in colunas if col != 'id']
    on_conflict = ', '.join(colunas_update)

    insert_sql = f"""
    INSERT INTO contribuintes2 ({', '.join(colunas)})
    VALUES ({placeholders}) 
    ON CONFLICT (id) DO UPDATE SET {on_conflict}
    """
    retorno = executa_query(cursor,insert_sql)
    return retorno