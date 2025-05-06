import json, math, requests, pyodbc, concurrent.futures, os, time
from rapidfuzz import fuzz


headers = {
        "Authorization": "",
        "Content-Type": "application/json"
        }

base_url_protocolo = 'https://api.protocolo.betha.cloud/protocolo/service-layer/v1/api/'
base_url_educacao = 'https://api.educacao.betha.cloud/educacao/service-layer/v1/api/'

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

def iniciarCursorPostgresql(host, banco_dados, porta, usuario, senha, driver="PostgreSQL Unicode"):
    conn_str = (
    f'DRIVER={driver};'
    f'UID={usuario};'
    f'PWD={senha};'
    f'Database={banco_dados};'
    f'Server={host};'
    f'Port={porta};'
)
    try:
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

def check_driver():
    drivers = pyodbc.drivers()
    print("Drivers ODBC disponíveis:")
    for driver in drivers:
        print(driver)

def pesquisa_all(url, token, offset, limit, todos=True):
    headers['Authorization'] = token
    url_final = url + "?limit=" + str(limit) + "&offset=" + str(offset)
    lista = []

    if todos:
        while True:
            try:
                response = requests.get(headers=headers, url=url_final)
                response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
                result = response.json()
                
                for registro in result['content']:
                    lista.append(registro)

                offset += limit
                url_final = url + "?limit=" + str(limit) + "&offset=" + str(offset)
                print('offset: ' + str(offset))
                if not result.get('hasNext', False):
                    break
            except requests.exceptions.RequestException as e:
                print(f"Erro ao fazer a requisição: {e}")
                break
    else:
        try:
            response = requests.get(url_final, headers=headers)
            response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
            result = response.json()
            if 'content' in result:
                for registro in result['content']:
                    lista.append(registro)
            else:
                lista.append(result)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")

    return lista

def criar_lotes(envios, tamanho_lote=99):
    if isinstance(envios, dict):
        envios = list(envios.values())
    lotes = [envios[i:i + tamanho_lote] for i in range(0, len(envios), tamanho_lote)]
    return lotes

def deletar_lotes(lotes: list, url, token):
    headers['Authorization']=token

    lista=[]
    for lote in lotes:
        json_string = json.dumps(lote, indent=4)
        # print(json_string)
        response = requests.delete(url, data=json_string, headers=headers)
        print(response.json())
        for item in lote:
            lista.append(response.json())
    return lista

def put_lotes(lotes: list, url, token):
    headers['Authorization']=token

    lista=[]
    print('Lotes a serem enviados:' + str(len(lotes)))

    def enviar_lote2(lote):
        json_string = json.dumps(lote, indent=4)

        with open('teste01.txt', 'w') as arquivo:
            arquivo.write(json_string)

        response = requests.put(url, data=json_string, headers=headers)
        return response.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(enviar_lote2, lote) for lote in lotes]
        for future in concurrent.futures.as_completed(futures):
            try:
                lista.append(future.result())
            except Exception as e:
                print(f"Erro ao enviar lote: {e}")

    return lista

def verifica_lotes(lotes: list, url, token):
    headers['Authorization']=token

    lista=[]
    while lotes:
    
        if len(lotes) >= 30:
            time.sleep(30)
        print('Quantidade de lotes no total faltantes: ' + str(len(lotes)))
        for lote in lotes:
            if 'message' in lote:
                if 'erro' in lote['message']:
                    lotes.remove(lote)
                    continue
            try:
                print(lote['id'])
                response = requests.get(url + lote['id'], headers=headers)
                status_code = response.status_code
                if status_code == 502:
                    lotes.remove(lote)
                    continue
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    print(f"Resposta recebida: {response.text}")
                    continue

                if status_code == 500:
                    lotes.remove(lote)
                    print('lote com erro')
                    print(lote)
                    continue

                if 'situacao' in response_json:
                    status = response_json['situacao']
                elif 'status' in response_json:
                    status = response_json['status']
                elif 'statusLote' in response_json:
                    status = response_json['statusLote']

                if status in ('EXECUTADO'):
                    lista.append(response)      
                    lotes.remove(lote)
                    continue

                if status in ('ERRO', 'ERROR'):
                    lotes.remove(lote)
                    print('lote com erro')
                    print(lote)
                    continue


            except requests.exceptions.RequestException as e:
                print(f"Erro ao fazer a requisição: {e}")
                continue



    return lista


def le_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        sql_script = file.read()
    return sql_script

def delete_all(url_busca: str, url_delete: str,url_busca_lote: str, token: str,  offset: int = 0, tamanho_lote_para_deletar: int = 99, limit: int = 99, tipo_json_montagem: int = 1,todos=True):
    headers['Authorization']=token
    pacote_deletar = []
    
    match tipo_json_montagem:
        case '1':
            json={
                "idIntegracao": None,
                "idGerado": None,
                "conteudo": None
            }
        case _:
            json={
                "idIntegracao": None,
                "idGerado": None,
                "conteudo": None
                }
    lista_para_deletar = pesquisa_all(url_busca,token,offset,limit,todos)

    for registro in lista_para_deletar:
    #     if registro["id"] >= 28030:
            json_novo = {}
            json_novo ["idIntegracao"] = registro["id"]
            json_novo ["idGerado"] = registro["id"]
            json_novo ["conteudo"] = registro
            pacote_deletar.append(json_novo)
    lotes_para_deletar = criar_lotes(pacote_deletar, tamanho_lote_para_deletar)
    lista_deletados = deletar_lotes(lotes_para_deletar, url_delete,token)
    return lista_deletados

def postar_lotes(lotes: list, url, token):                           
    headers['Authorization']=token

    lista=[]
    print('Lotes a serem enviados:' + str(len(lotes)))

    def enviar_lote(lote):
        json_string = json.dumps(lote, indent=4)

        with open('teste01.txt', 'w') as arquivo:
            arquivo.write(json_string)

        response = requests.post(url, data=json_string, headers=headers)
        return response.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(enviar_lote, lote) for lote in lotes]
        for future in concurrent.futures.as_completed(futures):
            try:
                lista.append(future.result())
            except Exception as e:
                print(f"Erro ao enviar lote: {e}")

    return lista

def postar_arquivo(lotes: list, url, token):                           
    headers['Authorization']=token
    headers.pop("Content-Type", None)  # Remover o Content-Type para permitir que requests defina automaticamente para multipart


    lista=[]
    print('Lotes a serem enviados:' + str(len(lotes)))

    def enviar_lote(lote):
        files = {
            "file": (lote[0]["nome_arquivo"], lote[0]["file"], "application/json")
        }
        data = {"idIntegracao":lote[0]["idIntegracao"]}

        # with open('teste01.txt', 'w') as arquivo:
            # arquivo.write(files)

        response = requests.post(url, files=files, data=data,headers=headers)
        return response.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(enviar_lote, lote) for lote in lotes]
        for future in concurrent.futures.as_completed(futures):
            try:
                lista.append(future.result())
            except Exception as e:
                print(f"Erro ao enviar lote: {e}")

    return lista


def postar_lotes_v3(cursor_envio,sistema,tabela,base_url,servico,lotes: list, token):
    base_url += servico
    lotes_enviar = criar_lotes(lotes,tamanho_lote=50)
    lotes_verificar = postar_lotes(lotes_enviar, base_url, token)
    lotes_verificados = verifica_lotes(lotes_verificar,base_url+'/lotes/',token)
    atualizar_retorno_lotes_tabela(cursor_envio,sistema,tabela,lotes_verificados,'post')

def postar_lotes_arquivos(cursor_envio,sistema,tabela,base_url,servico,lotes: list, token):
    base_url += servico
    lotes_enviar = criar_lotes(lotes,tamanho_lote=1)
    lotes_verificar = postar_arquivo(lotes_enviar, base_url, token)
    atualizar_retorno_arquivo_tabela(cursor_envio,sistema,tabela,lotes_verificar,'post')

def put_lotes_v2(base_url,servico,lotes: list, token):
    base_url += servico
    lotes_enviar = criar_lotes(lotes,tamanho_lote=50)
    lotes_verificar = put_lotes(lotes_enviar, base_url, token)
    lotes_verificados = verifica_lotes(lotes_verificar,base_url+'/lotes/',token)
    return lotes_verificados

def delete_lotes_v2(base_url,servico,lotes: list, token):
    base_url += servico
    lotes_enviar = criar_lotes(lotes)
    lotes_verificar = deletar_lotes(lotes_enviar, base_url, token)
    lotes_verificados = verifica_lotes(lotes_verificar,base_url+'/lotes/',token)
    return lotes_verificados

def executa_query(cursor,query):
    try:
        cursor.execute(query)
        quantidade = cursor.fetchall()
        return quantidade
    except pyodbc.Error as e:
        cursor.rollback()
        print("Erro ao executar SQL:", e)
        return False

def atualizar_retorno_lotes_tabela(cursor,sistema,tabela,lotes_processados, operacao):
    campo_atualizar = "id_gerado" if operacao == 'post' else "atualizado"
    
    for lote in lotes_processados:
        for item in lote.json()['retorno']:
            if item["situacao"] == "EXECUTADO":
                query = f"""update {sistema}.{tabela} set {campo_atualizar} = '{item["idGerado"]}' where id =  '{item["idIntegracao"]}' """
                cursor.execute(query)
                cursor.execute("commit;")
            print(item["mensagem"])


def atualizar_retorno_arquivo_tabela(cursor,sistema,tabela,lotes_processados, operacao):
    campo_atualizar = "id_gerado" if operacao == 'post' else "atualizado"
    
    for lote in lotes_processados:
        try:
            if lote["situacao"] == "EXECUTADO":
                query = f"""update {sistema}.{tabela} set {campo_atualizar} = '{lote["idGerado"]}' where id =  '{lote["idIntegracao"]}' """
                cursor.execute(query)
                cursor.execute("commit;")
            print(lote["mensagem"])
        except Exception as e:
            print(lote)

def delete_via_sql(cursor,sistema,tabela,url,token):
    lista=[]
    retorno = executa_query(cursor,f'''select id_gerado from {sistema}.{tabela} where id_gerado is not null and concorrente = 'SAAE' ''')
    for dado in retorno:
        json_montagem = {"idIntegraco": dado.id_gerado,"idGerado": dado.id_gerado,"conteudo":{"id": dado.id_gerado}}
        lista.append(json_montagem)
    deletar_lotes(criar_lotes(lista),url,token)
    
def iniciar_envio_total_v2(cursor_envio, enviar_json_funcao, sistema, tabela,servico, token, operacao):
    cursor_envio.execute(f"select protocolo.atualiza_id('{tabela}')")
    cursor_envio.execute("commit;")
    lista_enviar = enviar_json_funcao(cursor_envio,operacao)  
    sublistas = [lista_enviar[i:i + 20000] for i in range(0, len(lista_enviar), 20000)]

# Iterando sobre cada sublista para enviar os lotes
    for sublista in sublistas:
        start_time = time.time()
        postar_lotes_v3(
            cursor_envio, sistema, tabela, base_url_protocolo, servico, sublista, token
        )
        end_time = time.time()  # Capturar o tempo de fim
        elapsed_time = end_time - start_time  # Calcular o tempo gasto
        
        
        quantidade = executa_query(cursor_envio,f'''select count(*) from protocolo.{tabela} where id_gerado is null''')
        print('Tempo de processamento: ' + str(elapsed_time))
        print('Quantidade de registros faltantes a serem migrados: ' + str(quantidade[0][0]))


def iniciar_envio_total_arquivos(cursor_envio, enviar_json_funcao, sistema, tabela,servico, token, operacao):
    cursor_envio.execute(f"select protocolo.atualiza_id('{tabela}')")
    cursor_envio.execute("commit;")
    lista_enviar = enviar_json_funcao(cursor_envio,operacao)  
    sublistas = [lista_enviar[i:i + 100] for i in range(0, len(lista_enviar), 100)]

# Iterando sobre cada sublista para enviar os lotes
    for sublista in sublistas:
        start_time = time.time()
        postar_lotes_arquivos(
            cursor_envio, sistema, tabela, base_url_protocolo, servico, sublista, token
        )
        end_time = time.time()  # Capturar o tempo de fim
        elapsed_time = end_time - start_time  # Calcular o tempo gasto
        
        
        quantidade = executa_query(cursor_envio,f'''select count(*) from protocolo.{tabela} where id_gerado is null''')
        print('Tempo de processamento: ' + str(elapsed_time))
        print('Quantidade de registros faltantes a serem migrados: ' + str(quantidade[0][0]))


def iniciar_atualizacao_total_V2(cursor_envio, enviar_json_funcao, sistema, tabela,servico, token, operacao):
    cursor_envio.execute(f"select protocolo.atualiza_id('{tabela}')")
    cursor_envio.execute("commit;")
    lista_enviar = enviar_json_funcao(cursor_envio,operacao)  
    sublistas = [lista_enviar[i:i + 20000] for i in range(0, len(lista_enviar), 20000)]

# Iterando sobre cada sublista para enviar os lotes
    for sublista in sublistas:
        start_time = time.time()
        lotes_verificados = put_lotes_v2(base_url_protocolo,servico,sublista, token)
        atualizar_retorno_lotes_tabela(cursor_envio,sistema,tabela,lotes_verificados,'put')

        end_time = time.time()  # Capturar o tempo de fim
        elapsed_time = end_time - start_time  # Calcular o tempo gasto
        
        
        quantidade = executa_query(cursor_envio,f'''select count(*) from protocolo.{tabela} where atualizado is null''')
        print('Tempo de processamento: ' + str(elapsed_time))
        print('Quantidade de registros faltantes a serem migrados: ' + str(quantidade[0][0]))

def pesquisa_url_unitario(url, token, offset, limit):
    headers = {'Authorization': token}
    url_final = f"{url}?limit={limit}&offset={offset}"
    response = requests.get(headers=headers, url=url_final)
    print(offset)
    if response.status_code == 200:
        result = response.json()
        return result['content']
    else:
        return []

def pesquisa_all_simultaneo(url, token, offset, limit=99, max_workers=2, num_requisicoes=1):
    lista_final = []
    max_offset = limit * num_requisicoes

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for i in range(num_requisicoes):
            if offset > max_offset:
                break
            future = executor.submit(pesquisa_url_unitario, url, token, offset, limit)
            futures.append(future)
            offset += limit  

        while futures:
            done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                content = future.result()
                lista_final.extend(content)

    return lista_final

# def pesquisa_all_simultaneo_arquivos(url, token, offset, limit=1, max_workers=2, num_requisicoes=1):
#     lista_final = []
#     max_offset = limit * num_requisicoes

#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = []

#         for i in range(num_requisicoes):
#             if offset > max_offset:
#                 break
#             future = executor.submit(pesquisa_url_unitario, url+'/'+offset, token, offset, limit)
#             futures.append(future)
#             offset += limit  

#         while futures:
#             done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
#             for future in done:
#                 content = future.result()
#                 lista_final.extend(content)

#     return lista_final


def get_total_api_protocolo(url, token):
    headers['Authorization'] = token
    response = requests.get(headers=headers, url=url)
    result = response.json()['total']
    numero_lotes = math.ceil(response.json()['total'] / 99) + 1
    return result,numero_lotes



def realizar_pesquisa_funcionarios_atual(url_login,url_pesquisa,dados_login):

    headers_login = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    login = requests.post(url=url_login, data=dados_login, headers=headers_login)
    cookies = login.history[0].cookies.get_dict()['JSESSIONID']

    headers_pesquisa_dados = {
        'Cookie': f'JSESSIONID={cookies}'
    }

    resulto_pesquisa = requests.post(url=url_pesquisa, data=dados_login,headers=headers_pesquisa_dados)


    return resulto_pesquisa


def similaridade(nome1, nome2):
    """
    Compara dois nomes de estados brasileiros e retorna o grau de similaridade (0 a 100).
    """
    nome1 = nome1.strip().lower()
    nome2 = nome2.strip().lower()
    score = fuzz.WRatio(nome1, nome2)
    return score

def ler_arquivos_pasta(caminho_pasta):
    arquivos_conteudo = []
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        if os.path.isfile(caminho_arquivo):  # Verifica se é um arquivo
            with open(caminho_arquivo, 'rb') as arquivo:
                conteudo = arquivo.read()
                arquivos_conteudo.append({"nome_arquivo": nome_arquivo, "conteudo": conteudo})
    return arquivos_conteudo

def resgate_arquivos_pasta_local(cursor,caminho_absolute,tabela):
    # arquivos = executa_query(cursor,f'''select * from protocolo.{tabela} where arquivo is null''')
    lista_arquivos_pasta = ler_arquivos_pasta(caminho_absolute)
    
    for arquivo in lista_arquivos_pasta:
        try:
            id_arquivo = arquivo['nome_arquivo'].split("-")[0]
            print(f"Processando arquivo com ID: {id_arquivo}")

            query = f"""
                UPDATE protocolo.{tabela}
                SET arquivo = ?
                WHERE id = ?
                    AND arquivo IS NULL
                    AND id_gerado IS NULL
            """
            # Passar os parâmetros corretamente
            cursor.execute(query, (arquivo['conteudo'], id_arquivo))
            cursor.execute("COMMIT;")
            quantidade = executa_query(cursor,f'select count(*) from protocolo.{tabela} where arquivo is null')
            print(str(quantidade[0][0]))
        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo['nome_arquivo']}: {e}")


def criar_cursor(opcao):
    with open("config_banco.json", "r") as f:
        config = json.load(f)
    conf = config[opcao]
    conn = iniciarCursorPostgresql(banco_dados=conf["DATABASE"],
                            host=conf["SERVER"],
                            porta=conf["PORT"],
                            usuario=conf["UID"],
                            senha=conf["PWD"])
    return conn


def colunas_sql(cursor, sql):
    cursor.execute(sql)
    linhas = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    placeholders = ', '.join(['?'] * len(colunas))  # pyodbc usa '?'
    return placeholders, colunas, linhas

def execute_sql_extracao(cursor_extracao, cursor_envio, sql, tabela):

    placeholders, colunas, linhas = colunas_sql(cursor_extracao, sql)

    colunas_update = [f"{col} = EXCLUDED.{col}" for col in colunas if col != 'id']
    on_conflict = ', '.join(colunas_update)

    insert_sql = f"""
    INSERT INTO {tabela} ({', '.join(colunas)})
    VALUES ({placeholders}) 
    ON CONFLICT (id) DO UPDATE SET {on_conflict}
    """
    cursor_envio.executemany(insert_sql, linhas)
    return True


def ler_pasta_config_json(caminho):
    with open(caminho + '/' + 'config.json', 'r') as file:
        config = json.load(file)
    return config

def ler_servicos_json(config):
    return [{"nome": item["nome"], "tabela": item["tabela"]} for item in config["servicos"]]

def listrar_arquivos(caminho, extensao):
    arquivos = [arquivo for arquivo in os.listdir(caminho) if arquivo.endswith('.'+extensao)]
    return arquivos


def iniciar_extracao(servico, caminho):
    with open(caminho + '/' + 'SQL_Extracao' + '/' + servico["nome"] + '.sql', 'r', encoding='utf-8') as arquivo:
        script = arquivo.read()
    cursor_origem = criar_cursor('origem')
    cursor_destino = criar_cursor('destino')
    retorno = execute_sql_extracao(cursor_origem, cursor_destino, script, servico["tabela"])

    return True

def iniciar_envios(cursor, servico, funcao):
    print(servico, funcao)
    return True

def iniciar_atualizacao(cursor, servico, funcao):
    print(servico, funcao)
    return True

def iniciar_delete(cursor, servico, funcao):
    print(servico, funcao)
    return True