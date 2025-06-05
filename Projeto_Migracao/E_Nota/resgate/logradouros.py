# def atualiza_registro_lote(lote,cursor_resgate):
#     for registro in lote:
#         sql = '''Update "E_Nota".logradouros set id_gerado = ? 
#                 where unaccent(trim(lower(nome))) ilike unaccent(trim(lower(?))) 
#                 and estado_cloud_id = ?
#                 and id_gerado is null '''
#         params = (registro['id'],registro['nome'],registro['idEstado'])
#         cursor_resgate.execute(sql, params)
