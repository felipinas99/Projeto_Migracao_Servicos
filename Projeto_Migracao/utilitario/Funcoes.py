import json, requests, pyodbc, os, time, importlib, sqlparse

def iniciarCursorGeneric(host, banco_dados, porta, usuario, senha, driver):
    conn_str = (
        f'DRIVER={driver};'
        f'UID={usuario};'
        f'PWD={senha};'
        f'Database={banco_dados};'
        f'Server={host};'
        f'Port={porta};'
        f'ClientEncoding=UTF8;'  # Força a codificação UTF-8
    )
    try:
        pyodbc.setDecimalSeparator(".")
        conn = pyodbc.connect(conn_str)
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

def iniciarCursorPostgresql(host, banco_dados, porta, usuario, senha, driver="PostgreSQL UNICODE"):
    conn_str = (
        f'DRIVER={driver};'
        f'UID={usuario};'
        f'PWD={senha};'
        f'Database={banco_dados};'
        f'Server={host};'
        f'Port={porta};'
        f'ClientEncoding=UTF8;'  # Força a codificação UTF-8
    )
    try:
        pyodbc.setDecimalSeparator(".")
        conn = pyodbc.connect(conn_str)
        return conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        
def iniciarCursorSQLServer(host, banco_dados, usuario, senha, driver="ODBC Driver 17 for SQL Server"):
    conn_str = ( 
        f'DRIVER={driver};'
        f'SERVER={host};'
        f'DATABASE={banco_dados};'
        f'UID={usuario};'
        f'PWD={senha};'
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        
def iniciarCursorOracle(host, banco_dados, usuario, senha, driver="Oracle em OraDB19Home1"):
    conn_str = (
        f'DRIVER={driver};'
        f'DATABASE={banco_dados};'
        f'UID={usuario};'
        f'PWD={senha};'
        f'SERVER={host};'
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def busca_parametro(parametro):
    cursor = criar_cursor('destino')
    cursor.execute(f'''select * from motor.parametros where tipo_parametro = '{parametro}' ''')
    valor = cursor.fetchone().valor
    cursor.close()
    return valor

def envios(servico, caminho, funcao):
    try:
        metodo = ''
        cursor_insercao = criar_cursor('destino')
        cursor_controle_lotes = criar_cursor('destino')
        montagem = procura_montagem(servico)
        sistema = busca_parametro('Sistema')
        arquivo = os.path.join("Projeto_Migracao",sistema,"Sql_Envio",f"{servico['nome']}.sql")
        with open(arquivo, 'r', encoding='utf-8') as arquivo:
            script = arquivo.read()
            script_formatado = sqlparse.format(script, reindent=True, keyword_case='upper')

        if funcao == 'Atualizar':
            cursor_insercao.execute({script_formatado} + "not")
            metodo = 'PUT'
        else:
            cursor_insercao.execute(script_formatado)
            metodo = 'POST'
        while True:
            linhas = cursor_insercao.fetchmany(50)
            if not linhas:
                break
            
            lote = montagem.montar(linhas, funcao)
            sql = '''
                INSERT INTO motor.controle_lotes(metodo, tipo_registro, lote_envio)
                VALUES (?, ?, ?)
            '''
            params = (metodo, servico['tabela'], json.dumps(lote))
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
                    retorno, situacao = postar(url, lote.lote_envio, token, lote.tipo_registro, lote.metodo)
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
        return False

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

        situacao = resultado.get('situacao')
        match situacao:
            case 'EXECUTANDO':
                return resultado, 'PROCESSANDO'
            case 'ERRO' | 'ERROR':
                return resultado, 'ERRO'
            case 'EXECUTADO' | 'PROCESSADO' | 'EXECUTADO_OK':
                return resultado, 'PROCESSADO'
            case 'AGUARDANDO_EXECUCAO':
                return resultado, 'AGUARDANDO_EXECUCAO'
            case _:
                print(f"Situação desconhecida ou ausente: {situacao}")
                return resultado, 'ERRO'

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

def get_lotes():
    try:
        while True:
            cursor = criar_cursor('destino')
            cursor_atualiza = criar_cursor('destino')
            token  = busca_parametro('Token')
            url = busca_parametro('Url_Lote')
            cursor.execute('select * from motor.lotes_pendentes_processamento lpp')
            while True:
                lista = cursor.fetchmany(50)
                if not lista:
                    time.sleep(5)
                    break
                for lote in lista:
                    retorno, situacao = get_lote(url,lote.lote_id, token) 
                    if situacao in ('PROCESSADO','AGUARDANDO_EXECUCAO','EXECUTANDO'):
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
        return False
    
def atualiza_retorno_lote_itens():
    try:
        while True:
            cursor = criar_cursor('destino')
            cursor_atualiza = criar_cursor('destino')
            cursor.execute('select * from motor.lotes_pendentes_resgate lpp')
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
                        if item.get("idGerado") == None:
                            sql = f'''UPDATE controle.{lote.tipo_registro} set mensagem = ? where id = ?'''
                            params = (mensagem, item['idIntegracao'])
                        else:
                            sql = f'''UPDATE controle.{lote.tipo_registro} set id_gerado = ? , mensagem = ? where id = ?'''
                            params = (item['idGerado'], mensagem ,item['idIntegracao'])
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
        return False

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
    sql = sql.encode('utf-8', errors='replace').decode('utf-8')
    cursor.execute(sql)
    linhas = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    return colunas, linhas

def execute_sql_extracao(cursor_extracao, cursor_envio, sql, tabela, tamanho_sql=1000):
    colunas, linhas = colunas_sql(cursor_extracao, sql)

    colunas_update = [f"{col} = EXCLUDED.{col}" for col in colunas if col != 'id']
    on_conflict = ', '.join(colunas_update)

    colunas_sql_str = ', '.join(colunas)
    linha_placeholder = f"({', '.join(['?'] * len(colunas))})"

    for i in range(0, len(linhas), tamanho_sql):
        batch = linhas[i:i + tamanho_sql]

        all_placeholders = ', '.join([linha_placeholder] * len(batch))
        flat_values = [valor for linha in batch for valor in linha]  

        insert_sql = f"""
        INSERT INTO controle.{tabela} ({colunas_sql_str})
        VALUES {all_placeholders}
        ON CONFLICT (id) DO UPDATE SET {on_conflict}
        """

        cursor_envio.execute(insert_sql, flat_values)

    cursor_envio.execute("commit")

def procura_montagem(nome_arquivo):
    sistema = busca_parametro('Sistema')
    arquivo = os.path.join("Projeto_Migracao",sistema,"Json_envio",f"{nome_arquivo['nome']}")
    modulo_nome = arquivo.replace("\\", ".").replace("/", ".")
    modulo = importlib.import_module(modulo_nome)
    return modulo

def ler_pasta_config_json(caminho):
    print(os.path.abspath(os.path.dirname(__file__)))
    with open(caminho + '/' + 'config.json', 'r') as file:
        config = json.load(file)
    return config

def ler_servicos_json(config):
    return [{"nome": item["nome"], "tabela": item["tabela"]} for item in config["servicos"]]


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
        cursor_destino = criar_cursor('destino')
        execute_sql_extracao(cursor_origem, cursor_destino, script_formatado, servico["tabela"])
    except Exception as e:
        print(f"Erro ao executar a extração: {e}")
        return False
    finally:
        cursor_origem.close()
        cursor_destino.close()
    return True

def iniciar_envios(servico, caminho, funcao):
    return envios(servico, caminho, funcao)

def iniciar_atualizacao(servico, caminho, funcao):
    return envios(servico, caminho, funcao)

def iniciar_delete(cursor, servico, funcao):
    print(servico, funcao)
    return True