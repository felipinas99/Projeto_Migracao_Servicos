def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote['conteudo']:
        sql = '''Update "Livro_Eletronico".estados set 
        id_gerado = ? where unaccent(trim(lower(nome))) 
        ilike unaccent(trim(lower(?))) 
        and id_gerado is null '''
        params = (registro['idGerado']['iEstados'],registro['nome'])
        cursor_resgate.execute(sql, params)
