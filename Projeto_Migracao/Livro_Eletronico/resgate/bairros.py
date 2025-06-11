def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote['conteudo']:
        sql = '''Update "Livro_Eletronico".bairros set id_gerado = ? 
                where REGEXP_REPLACE(unaccent(trim(lower(nome))), '[ªº°§]', '', 'g') ilike REGEXP_REPLACE(unaccent(trim(lower(?))) , '[ªº°§]', '', 'g')
                and municipio_cloud_id = ?
                and id_gerado is null '''
        params = (registro['idGerado']['iBairros'],registro['nome'],registro['codigoMunicipio'])
        cursor_resgate.execute(sql, params)
