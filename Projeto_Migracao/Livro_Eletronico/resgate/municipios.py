def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote['conteudo']:
        sql = '''Update "Livro_Eletronico".municipios set id_gerado = ? 
                where unaccent(trim(lower(nome))) ilike unaccent(trim(lower(?))) 
                and estado_cloud_id = ?
                and id_gerado is null '''
        params = (registro['idGerado']['iMunicipios'],registro['nome'],registro['codigoEstado'])
        cursor_resgate.execute(sql, params)
