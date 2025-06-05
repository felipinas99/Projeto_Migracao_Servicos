def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote:
        sql = '''Update "E_Nota".pessoas set id_gerado = ? 
        where inscricao ilike ?
        and id_gerado is null '''
        params = (registro['id'],registro['inscricao'])
        cursor_resgate.execute(sql, params)
