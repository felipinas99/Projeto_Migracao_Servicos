def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote:
        sql = '''Update "E_Nota".estados set id_gerado = ? where unaccent(trim(lower(nome))) ilike unaccent(trim(lower(?))) and id_gerado is null '''
        params = (registro['id'],registro['nome'])
        cursor_resgate.execute(sql, params)
