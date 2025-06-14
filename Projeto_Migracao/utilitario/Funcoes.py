import json, requests, pyodbc, os, time, importlib, sqlparse, sys,  csv , psycopg2 , tempfile, os,concurrent.futures

def iniciarCursorGeneric(host, banco_dados, porta, usuario, senha, driver):
    conn_str = (
        f'DRIVER={driver};'
        f'UID={usuario};'
        f'PWD={senha};'
        f'Database={banco_dados};'
        f'Server={host};'
        f'Port={porta};'
        f'ClientEncoding=UTF8;'
        # f'MARS_Connection=yes;' 
    )
    try:
        pyodbc.setDecimalSeparator(".")
        conn = pyodbc.connect(conn_str)
        return conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def iniciarCursorPostgresql(host, banco_dados, porta, usuario, senha):
    try:
        conn = psycopg2.connect(user=usuario,
        password=senha,
        dbname=banco_dados,
        host=host,
        port=int(porta))
        return conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def iniciarCursorSybase(dsn, usuario, senha, app="APP=BTLS=V2Y7Uq9RxaIfCU87u8ugNIW+/03ctxUc6nfxu9n2Qu9omwxmbQccTa3e2zujHW+PFBkBuXBQPnwIDpKrTdNusi811gsL3cvJ/vOOYqOAA5rqDBz4AElLxstkQXonzuc9twe54bkelHF2DpZj4B8M6NmHM4v2RO6PCuRH/fTqFAA=", driver ="SQL Anywhere 16"):
    
    stringCon = 'DRIVER=' + driver + ';SERVER=' + dsn  + ';DSN=' + dsn + ';Uid=' + usuario + ';Pwd=' + senha + ';Encrypt=yes;Connection Timeout=30;APP='+ app +';'
    qtd_try = 0
    conn = None
    while not conn:
        qtd_try += 1
        try:
            conn = pyodbc.connect(stringCon)
        except Exception as i:
            print(i)
        
        if qtd_try > 20:
            print("Erro crítico ao conectar com banco de dados. Abortando execução...")
            exit()
    cursor = conn.cursor()

    return cursor        

def busca_parametro(parametro):
    cursor = criar_cursor('destino')
    cursor.execute(f'''select * from motor.parametros where tipo_parametro = '{parametro}' ''')
    valor = cursor.fetchone().valor
    cursor.close()
    return valor

def envios(servico, funcao):
    try:
        metodo = ''
        cursor_insercao = criar_cursor('destino')
        cursor_controle_lotes = criar_cursor('destino')
        montagem = procura_montagem(servico,'Json_envio')
        sistema = busca_parametro('Sistema')
        arquivo = os.path.join("Projeto_Migracao",sistema,"Sql_Envio",f"{servico['nome']}.sql")

        with open(arquivo, 'r', encoding='utf-8') as arquivo:
            script = arquivo.read()

        if funcao == 'Atualizar':
            cursor_insercao.execute(script[:-4] + " not " + script[-4:])
            metodo = 'PUT'
        else:
            cursor_insercao.execute(script)
            metodo = 'POST'
        while True:
            linhas = cursor_insercao.fetchmany(50)
            if not linhas:
                break
            lote = montagem.montar(linhas, funcao)
            sql = '''
                INSERT INTO motor.controle_lotes(sistema, metodo, tipo_registro, servico, lote_envio)
                VALUES (?, ?, ?, ?, ?)
            '''
            params = (sistema, metodo, servico['tabela'],servico['servico'], json.dumps(lote, default=str))
            cursor_controle_lotes.execute(sql, params)
            cursor_controle_lotes.execute("commit;")
        cursor_insercao.close()
        cursor_controle_lotes.close()
    except Exception as e:
        cursor_insercao.close()
        cursor_controle_lotes.close()
        print(f"Erro ao executar a inserção: {e}")
        return False
    return True

def postar(url,lote,token,servico, metodo):
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
        }           
            
    headers['Authorization']=f'Bearer {token}'

    try:
        if metodo == 'PUT':
            response = requests.put(url+servico, data=lote, headers=headers)
        else:
            response = requests.post(url+servico, data=lote, headers=headers)
        retorno = response.json()
        id_lote = retorno.get('id') or retorno.get('idLote')
        if id_lote != None:
            return retorno, 'ENVIADO'
        return retorno, 'ERRO'
    except Exception as e:
        return 'erro'

def postagem():
    try:
        while True:
            cursor = criar_cursor('destino')
            cursor_atualiza = criar_cursor('destino')
            token  = busca_parametro('Token')
            url = busca_parametro('Url_Base')
            cursor.execute('select * from motor.lotes_pendentes_envio')
            while True:
                lista = cursor.fetchmany(50)
                if not lista:
                    time.sleep(5)
                    break
                for lote in lista:
                    retorno, situacao = postar(url, lote.lote_envio, token, lote.servico, lote.metodo)
                    id_lote = retorno.get('id') or retorno.get('idLote')
                    sql = '''UPDATE motor.controle_lotes set status_envio = ?, lote_id = ?, lote_envio_retorno = ?  where id = ?'''
                    params = (situacao, id_lote, json.dumps(retorno), lote.id)
                    cursor_atualiza.execute(sql, params)
                    cursor_atualiza.execute("commit")
            
            cursor.close()
            cursor_atualiza.close()
    except Exception as e:
        cursor.close()
        cursor_atualiza.close()
        print(f"Erro postagem: {e}")
        time.sleep(5)
        postagem()

def get_lote(url, lote_id, token):
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
        }

    headers['Authorization']=f'Bearer {token}'

    try:
        response = requests.get(
            url=f'{url}{lote_id}',
            headers=headers
        )
        resultado = response.json()

        situacao = resultado.get('situacao') or resultado.get('statusLote')
        match situacao:
            case 'EXECUTANDO' | 'EM PROCESSAMENTO':
                return resultado, 'PROCESSANDO' 
            case 'ERRO' | 'ERROR':
                return resultado, 'ERRO'
            case 'EXECUTADO' | 'PROCESSADO' | 'EXECUTADO_OK'| 'EXECUTADO_PARCIALMENTE_OK':
                return resultado, 'PROCESSADO'
            case 'AGUARDANDO_EXECUCAO':
                return resultado, 'AGUARDANDO_EXECUCAO'
            case _:
                print(f"Situação desconhecida ou ausente: {situacao}")
                return resultado, 'DESCONHECIDO'

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return {}, 'ERRO'
    except ValueError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print(f"Resposta bruta (para análise): {response.text}")
        return {}, 'ERRO'
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return {}, 'ERRO'

def get_lotes_paralelo():
    def processa_lote(lote):
        try:
            cursor_atualiza = criar_cursor('destino')  # Cada thread cria seu próprio cursor!
            retorno, situacao = get_lote(url, lote.lote_id, token)
            if situacao in ('PROCESSADO','AGUARDANDO_EXECUCAO','EXECUTANDO','PROCESSANDO'):
                sql = '''UPDATE motor.controle_lotes set status_envio = ?, lote_recebido = ? where id = ?'''
                params = (situacao, json.dumps(retorno), lote.id)
                cursor_atualiza.execute(sql, params)
                cursor_atualiza.execute("commit")
            cursor_atualiza.close()
        except Exception as e:
            print(f"Erro no processamento do lote {getattr(lote, 'id', None)}: {e}")


    try:
        while True:
            cursor = criar_cursor('destino')
            token  = busca_parametro('Token')
            sistema  = busca_parametro('Sistema')
            url = busca_parametro('Url_Lote')
            cursor.execute(f'''select * from motor.lotes_pendentes_processamento lpp where sistema = '{sistema}' ''')
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                while True:
                    lista = cursor.fetchmany(50)
                    if not lista:
                        time.sleep(5)
                        break
                    executor.map(processa_lote, lista)
            cursor.close()
    except Exception as e:
        print(f"Erro ao get_lotes: {e}")
        time.sleep(5)
        get_lotes_paralelo()

def get_lotes():
    try:
        while True:
            cursor = criar_cursor('destino')
            cursor_atualiza = criar_cursor('destino')
            token  = busca_parametro('Token')
            sistema  = busca_parametro('Sistema')
            url = busca_parametro('Url_Lote')
            cursor.execute(f'''select * from motor.lotes_pendentes_processamento lpp where sistema = '{sistema}' ''')
            while True:
                lista = cursor.fetchmany(50)
                if not lista:
                    time.sleep(5)
                    break
                for lote in lista:
                    retorno, situacao = get_lote(url,lote.lote_id, token) 
                    if situacao in ('PROCESSADO','AGUARDANDO_EXECUCAO','EXECUTANDO','PROCESSANDO'):
                        sql = '''UPDATE motor.controle_lotes set status_envio = ?, lote_recebido = ? where id = ?'''
                        params = (situacao, json.dumps(retorno), lote.id)
                        cursor_atualiza.execute(sql, params)
                        cursor_atualiza.execute("commit")
                        continue
            cursor.close()
            cursor_atualiza.close()
    
    except Exception as e:
        cursor.close()
        cursor_atualiza.close()
        print(f"Erro ao get_lotes: {e}")
        time.sleep(5)
        get_lotes()
    
def atualiza_retorno_lote_itens():
    try:
        while True:
            cursor = criar_cursor('destino')
            cursor_atualiza = criar_cursor('destino')
            sistema = busca_parametro('Sistema')
            cursor.execute(f'''select * from motor.lotes_pendentes_resgate lpp where sistema = '{sistema}' ''')
            while True:
                lista = cursor.fetchmany(50)
                if not lista:
                    time.sleep(5)
                    break
                for lote in lista:
                    retorno = json.loads(lote.lote_recebido)['retorno']
                    if not retorno:
                        continue

                    for item in retorno:
                        mensagem =  str(item.get("situacao")) + ' / '  + str(item.get("mensagem"))
                        id_gerado = item.get('idGerado', {}).get('id') or item.get('idGerado', {}).get('ids') or item.get("idGerado") 
                        if isinstance(id_gerado, dict):
                            id_gerado = id_gerado.get('i'+str(lote.tipo_registro).capitalize())
                            # id_gerado = json.dumps(id_gerado, default=str)
                            if id_gerado == None:
                                id_gerado = json.dumps(item.get("idGerado"))



                        if id_gerado == None:
                            sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set mensagem = ? where id = ?'''
                            params = (mensagem, item['idIntegracao'])
                            if item.get("status") == 'SUCESSO':
                                sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set mensagem = ? , atualizado = 'true'  where id = ?'''
                                params = (mensagem, item['idIntegracao'])
                        else:
                            sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set id_gerado = ? , mensagem = ?, atualizado = 'true' where id = ?'''
                            params = (str(id_gerado), mensagem ,item['idIntegracao'])
                            
                        cursor_atualiza.execute(sql, params) 
                        cursor_atualiza.execute("commit")

                    sql = f'''UPDATE motor.controle_lotes set ids_atualizados = true where id = ?'''
                    params = (lote.id)
                    cursor_atualiza.execute(sql, params)
                    cursor_atualiza.execute("commit")
            cursor.close()
            cursor_atualiza.close()
    except Exception as e:
        cursor.close()
        cursor_atualiza.close()
        print(f"Erro ao atualiza_retorno_lote_itens: {e}")
        time.sleep(5)
        atualiza_retorno_lote_itens()

def criar_cursor(opcao):
    with open("Projeto_Migracao/config_banco.json", "r") as f:
        config = json.load(f)
    conf = config[opcao]
    cursor = iniciarCursorGeneric(banco_dados=conf["DATABASE"],
                            host=conf["SERVER"],
                            porta=conf["PORT"],
                            usuario=conf["UID"],
                            senha=conf["PWD"],
                            driver=conf["DRIVER"])
    return cursor

def colunas_sql(cursor, sql):
    
    inicio = time.time()  # Início da contagem do tempo
    sql = sql.encode('utf-8', errors='replace').decode('utf-8')
    cursor.execute(sql)
    linhas = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    
    fim = time.time()  # Fim da contagem do tempo
    print(f"Tempo de execução: {fim - inicio:.2f} segundos")


    return colunas, linhas

def execute_sql_extracao(cursor_extracao, sql, tabela):

    with open("Projeto_Migracao/config_banco.json", "r") as f:
        config = json.load(f)
    conf = config['destino']


    cursor = iniciarCursorPostgresql(banco_dados=conf["DATABASE"],
                            host=conf["SERVER"],
                            porta=conf["PORT"],
                            usuario=conf["UID"],
                            senha=conf["PWD"])


    sistema = busca_parametro('Sistema')
    colunas, linhas = colunas_sql(cursor_extracao, sql)
    colunas_sql_str = ', '.join(colunas)
    temp_table = f"temp_{tabela}"

    
    start_time = time.time()

    # 1. Crie uma tabela temporária
    cursor.execute(f'DROP TABLE IF EXISTS {temp_table}')
    cursor.execute(f'CREATE TEMP TABLE {temp_table} AS SELECT * FROM "{sistema}".{tabela} LIMIT 0')

    # 2. Escreva os dados em um arquivo CSV temporário
    with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(linhas)
        temp_csv_path = csvfile.name

    # 3. Use COPY para inserir rapidamente na tabela temporária
    conn = cursor.connection
    with open(temp_csv_path, 'r', encoding='utf-8') as f:
        with conn.cursor() as psy_cursor:
            psy_cursor.copy_expert(
                f"COPY {temp_table} ({colunas_sql_str}) FROM STDIN WITH CSV",
                f
            )
        conn.commit()

    # 4. Faça o upsert (merge) dos dados da tabela temporária para a tabela final
    colunas_update = [f"{col} = EXCLUDED.{col}" for col in colunas if col != 'id']
    on_conflict = ', '.join(colunas_update)
    insert_sql = f'''
        INSERT INTO "{sistema}".{tabela} ({colunas_sql_str})
        SELECT {colunas_sql_str} FROM {temp_table}
        ON CONFLICT (id) DO UPDATE SET {on_conflict}
    '''
    cursor.execute(insert_sql)
    cursor.execute("commit")

    # 5. Limpeza
    os.remove(temp_csv_path)

    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tempo decorrido: {elapsed_time} segundos")

def procura_montagem(nome_arquivo, pasta):
    sistema = busca_parametro('Sistema')
    arquivo = os.path.join("Projeto_Migracao",sistema,pasta,f"{nome_arquivo['nome']}")
    modulo_nome = arquivo.replace("\\", ".").replace("/", ".")
    if modulo_nome in sys.modules:
        importlib.reload(sys.modules[modulo_nome])
    else:
        importlib.import_module(modulo_nome)
    modulo = sys.modules[modulo_nome]
    return modulo

def ler_pasta_config_json(caminho):
    print(os.path.abspath(os.path.dirname(__file__)))
    with open(caminho + '/' + 'config.json', 'r') as file:
        config = json.load(file)
    return config

def ler_servicos_json(config):
    return [{"nome": item["nome"], "tabela": item["tabela"], "servico": item["servico"]} for item in config["servicos"]]

def get_unitario(url, headers, sistema):

    response = requests.get(headers=headers, url=url)
    if response.status_code == 200:
        result = response.json()

        match sistema:
            case 'Protocolo':
                if result == []:
                    return result, False
            case 'Livro_Eletronico':
                if result['conteudo'] == []:
                    return result['conteudo'], False
        return result, True

def busca_todos_registros_cloud(servico):
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }
    try:
        continuar = True
        url = busca_parametro('Url_Base')
        token = busca_parametro('Token')
        sistema = busca_parametro('Sistema')
        headers['Authorization'] = f'Bearer {token}'
        limit = 99
        offset = 0
        url_final = url + servico["servico"]
        match sistema:
            case 'Protocolo':
                url_final += "?limit={limit}&offset={offset}"
            case 'Livro_Eletronico' | 'E_Nota':
                offset = 1
                url_final += "?nRegistros={limit}&iniciaEm={offset}"

        while continuar:
            url_pagina = url_final.format(limit=limit, offset=offset)
            retorno, continuar = get_unitario(url_pagina, headers, sistema)
            if not retorno or retorno == []:
                break
            yield retorno 
            offset += limit
    except Exception as e:
        print(f"Erro na busca_todos_registros_cloud: {e}")
        return

def atualiza_dependencias_tabela_controle(servico,sistema):
    try:
        cursor_destino = criar_cursor('destino')

        arquivo_atualizar_dependencias = os.path.join("Projeto_Migracao",sistema,"Atualizar_Dependencias.sql")
        with open(arquivo_atualizar_dependencias, 'r', encoding='utf-8') as arquivo_atualizar_dependencias:
            script = arquivo_atualizar_dependencias.read()
            script_formatado2 = sqlparse.format(script, reindent=True, keyword_case='upper')
        cursor_destino = criar_cursor('destino')
        cursor_destino.execute(script_formatado2)
        cursor_destino.execute("commit;")
        cursor_destino.execute(f'''select "{sistema}".atualizar_dependencias('{servico['tabela']}', '{sistema}')''')
        cursor_destino.execute("commit;")

    except Exception as e:
        print(f"Erro ao executar a resgate: {e}")
        return False
    finally:
        cursor_destino.close()

def resgate(servico):
    try:
        cursor_resgate = criar_cursor('destino')
        montagem = procura_montagem(servico,'resgate')
        for lote in busca_todos_registros_cloud(servico):
            montagem.atualiza_registro_lote(lote,cursor_resgate)
            cursor_resgate.commit()

        return True
    except Exception as e:
        print(f"Erro ao executar a resgate: {e}")
        return False
    finally:
        cursor_resgate.close()

def listrar_arquivos(caminho, extensao):
    arquivos = [arquivo for arquivo in os.listdir(caminho) if arquivo.endswith('.'+extensao)]
    return arquivos

def iniciar_extracao(**kwargs):
    servico = kwargs.get("servico")
    try:
        sistema = busca_parametro('Sistema')
        concorrente = busca_parametro('Concorrente')
        arquivo = os.path.join("Projeto_Migracao",sistema,"Concorrente_Extracao",concorrente,f"{servico['nome']}.sql")
        with open(arquivo, 'r', encoding='utf-8') as arquivo:
            script = arquivo.read()
            script_formatado = sqlparse.format(script, reindent=True, keyword_case='upper')
        cursor_origem = criar_cursor('origem')
        execute_sql_extracao(cursor_origem, script_formatado, servico["tabela"])
        atualiza_dependencias_tabela_controle(servico, sistema)
        
    except Exception as e:
        print(f"Erro ao executar a extração: {e}")
        return False
    finally:
        cursor_origem.close()

    return True

def iniciar_envios(**kwargs):

    sistema = busca_parametro('Sistema')
    servico = kwargs.get("servico")
    funcao = kwargs.get("funcao")
    atualiza_dependencias_tabela_controle(servico,sistema)


    return envios(servico, funcao)

def iniciar_resgate(**kwargs):
    servico = kwargs.get("servico")
    sistema = busca_parametro('Sistema')
    atualiza_dependencias_tabela_controle(servico,sistema)
    return resgate(servico)

def iniciar_atualizacao(**kwargs):
    servico = kwargs.get("servico")
    funcao = kwargs.get("funcao")
    sistema = busca_parametro('Sistema')
    atualiza_dependencias_tabela_controle(servico,sistema)
    return envios(servico, funcao)

def iniciar_delete(**kwargs):
    servico = kwargs.get("servico")
    funcao = kwargs.get("funcao")
    print(servico, funcao)
    return True