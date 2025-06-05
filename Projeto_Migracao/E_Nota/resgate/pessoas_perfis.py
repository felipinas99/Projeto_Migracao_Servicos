def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote:
        sql = '''Update "E_Nota".pessoas_perfis set id_gerado = ? 
        where pessoa_cloud_id = ?
        and id_gerado is null '''
        params = (registro['id'],registro['idPessoa'])
        cursor_resgate.execute(sql, params)
