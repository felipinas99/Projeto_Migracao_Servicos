def atualiza_registro_lote(lote,cursor_resgate):
    for registro in lote['conteudo']:
        if registro['tipoPessoa'] == 'J':
            cnpj = registro.get('pessoaJuridica', {}).get('cnpj')
            if cnpj is not None:
                sql = '''Update "Livro_Eletronico".pessoas set id_gerado = ? 
                where cpf_cnpj = ?
                and id_gerado is null '''
                params = (registro['idGerado']['iPessoas'], registro['pessoaJuridica']['cnpj'])
                cursor_resgate.execute(sql, params)
        if registro['tipoPessoa'] == 'F' and registro['pessoaFisica'] is not None: 
            cpf = registro.get('pessoaFisica', {}).get('cpf')
            if cpf is not None:
                sql = '''Update "Livro_Eletronico".pessoas set id_gerado = ? 
                where cpf_cnpj = ?
                and id_gerado is null '''
                params = (registro['idGerado']['iPessoas'], registro['pessoaFisica']['cpf'])
                cursor_resgate.execute(sql, params)
