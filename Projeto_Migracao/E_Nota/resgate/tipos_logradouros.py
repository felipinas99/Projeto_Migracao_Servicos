def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote:
        sql = '''Update "E_Nota".tipos_logradouros set id_gerado = ? 
        where unaccent(trim(lower(descricao))) ilike unaccent(trim(lower(?))) 
        and id_gerado is null '''
        params = (registro['id'],registro['descricao'])
        cursor_resgate.execute(sql, params)
