def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote:
        sql = '''Update "E_Nota".listas_servicos_entidades set id_gerado = ? 
        where codigo = ?
        and listas_servicos_leis_cloud_id = ?
        and id_gerado is null '''
        params = (registro['id'],registro['codigo'],registro['idListasServicosLeis'])
        cursor_resgate.execute(sql, params)
