import os
import threading

import sqlparse
from Projeto_Migracao.utilitario.Funcoes import busca_parametro, criar_cursor, envios, execute_sql_extracao, resgate
import json
import time
import requests
from Projeto_Migracao.utilitario.motor import Motor

class ProcessamentoController(Motor):
    def __init__(self):
        self.threads: list[threading.Thread] = []
        self.status_postagem: bool = True
        self.cursor: pyodbc.Cursor | None = None # type: ignore
        self.cursor_atualiza: pyodbc.Cursor | None = None # type: ignore


    def start(self):
        self.checa_motor()
        if self.motor_construido is False:
            return
        else:
            self.token = busca_parametro('Token')
            self.url_envio = busca_parametro('Url_Base')
            self.url_lote = busca_parametro('Url_Lote')
            self.sistema = busca_parametro('Sistema')
            self.concorrente = busca_parametro('Concorrente')
            self.threads = [
                threading.Thread(target=self.postagem, daemon=True),
                threading.Thread(target=self.get_lotes, daemon=True),
                threading.Thread(target=self.atualiza_retorno_lote_itens, daemon=True)
            ]
            for t in self.threads:
                t.start()

    def join(self):
        for t in self.threads:
            t.join()

    def postar(self, url, lote, token, servico, metodo):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            if metodo == 'PUT':
                response = requests.put(url + servico, data=lote, headers=headers)
            else:
                response = requests.post(url + servico, data=lote, headers=headers)
            retorno = response.json()
            id_lote = retorno.get('id') or retorno.get('idLote')
            if id_lote is not None:
                return retorno, 'ENVIADO'
            return retorno, 'ERRO'
        except Exception as e:
            print(f"Erro ao postar lote: {e}")
            return 'erro', 'ERRO'

    def postagem(self):
        try:
            while True:
                if self.motor_construido is False:
                    break
                cursor = criar_cursor('destino')
                cursor_atualiza = criar_cursor('destino')
                cursor.execute('select * from motor.lotes_pendentes_envio where sistema = ? order by 1 asc', self.sistema)
                while True:
                    lista = cursor.fetchmany(50)
                    if not lista:
                        time.sleep(5)
                        break
                    for lote in lista:
                        if self.status_postagem is False:
                            print("Postagem interrompida manualmente.")
                            break
                        retorno, situacao = self.postar(self.url_envio, lote.lote_envio, self.token, lote.servico, lote.metodo)
                        id_lote = retorno.get('id') or retorno.get('idLote') if isinstance(retorno, dict) else None
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
            self.postagem()

    def get_lotes(self):
        try:
            while True:
                if self.motor_construido is False:
                    break
                cursor = criar_cursor('destino')
                cursor_atualiza = criar_cursor('destino')
                cursor.execute(f'''select * from motor.lotes_pendentes_processamento lpp where sistema = '{self.sistema}' ''')
                while True:
                    lista = cursor.fetchmany(50)
                    if not lista:
                        time.sleep(5)
                        break
                    for lote in lista:
                        retorno, situacao = self.get_lote(self.url_lote, lote.lote_id, self.token)
                        if situacao in ('PROCESSADO', 'AGUARDANDO_EXECUCAO', 'EXECUTANDO', 'PROCESSANDO'):
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
            self.get_lotes()

    def get_lote(self, url, lote_id, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
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
                case 'EXECUTADO' | 'PROCESSADO' | 'EXECUTADO_OK' | 'EXECUTADO_PARCIALMENTE_OK':
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

    def atualiza_retorno_lote_itens(self):
        try:
            while True:
                if self.motor_construido is False:
                    break
                cursor = criar_cursor('destino')
                cursor_atualiza = criar_cursor('destino')
                cursor.execute(f'''select * from motor.lotes_pendentes_resgate lpp where sistema = '{self.sistema}' ''')
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
                            mensagem = str(item.get("situacao")) + ' / ' + str(item.get("mensagem"))
                            id_gerado = item.get('idGerado', {}).get('id') or item.get('idGerado', {}).get('ids') or item.get("idGerado")
                            if isinstance(id_gerado, dict):
                                id_gerado = id_gerado.get('i' + str(lote.tipo_registro).capitalize())
                                if id_gerado is None:
                                    id_gerado = json.dumps(item.get("idGerado"))
                            if id_gerado is None:
                                sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set mensagem = ? where id = ?'''
                                params = (mensagem, item['idIntegracao'])
                                if item.get("status") == 'SUCESSO':
                                    sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set mensagem = ? , atualizado = 'true'  where id = ?'''
                                    params = (mensagem, item['idIntegracao'])
                            else:
                                sql = f'''UPDATE "{lote.sistema}".{lote.tipo_registro} set id_gerado = ? , mensagem = ?, atualizado = 'true' where id = ?'''
                                params = (str(id_gerado), mensagem, item['idIntegracao'])
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
            self.atualiza_retorno_lote_itens()

    def iniciar_extracao(self, **kwargs):
        servico = kwargs.get("servico")
        try:
            arquivo = os.path.join("Projeto_Migracao",self.sistema,"Concorrente_Extracao",self.concorrente,f"{servico['nome']}.sql")
            with open(arquivo, 'r', encoding='utf-8') as arquivo:
                script = arquivo.read()
                script_formatado = sqlparse.format(script, reindent=True, keyword_case='upper')
            cursor_origem = criar_cursor('origem')
            execute_sql_extracao(cursor_origem, script_formatado, servico["tabela"])
            self.atualiza_dependencias_tabela_controle(servico, self.sistema)
            
        except Exception as e:
            print(f"Erro ao executar a extração: {e}")
            return False
        finally:
            cursor_origem.close()
        
    def iniciar_envios(self,**kwargs):
        servico = kwargs.get("servico")
        funcao = kwargs.get("funcao")
        self.atualiza_dependencias_tabela_controle(servico,self.sistema)
        return envios(servico, funcao)

    def iniciar_resgate(self,**kwargs):
        servico = kwargs.get("servico")
        self.atualiza_dependencias_tabela_controle(servico,self.sistema)
        return resgate(servico)

    def iniciar_atualizacao(self, **kwargs):
        servico = kwargs.get("servico")
        funcao = kwargs.get("funcao")
        self.atualiza_dependencias_tabela_controle(servico,self.sistema)
        return envios(servico, funcao)

    def salvar_retorno_sql_em_txt(self,retorno_sql, nome_arquivo="resultado_pre_validacao.txt"):
        """
        Salva o retorno do SQL em um arquivo .txt na pasta 'pre_validacao' duas pastas acima do arquivo atual.
        """
        # Caminho para duas pastas acima
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        pasta_pre_validacao = os.path.join(base_dir, "Pre_Validacao")
        os.makedirs(pasta_pre_validacao, exist_ok=True)

        caminho_arquivo = os.path.join(pasta_pre_validacao, nome_arquivo)

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            if isinstance(retorno_sql, (list, tuple)):
                for linha in retorno_sql:
                    f.write(str(linha) + "\n")
            else:
                f.write(str(retorno_sql))

        print(f"Arquivo salvo em: {caminho_arquivo}")


    def iniciar_pre_validacao(self, **kwargs):
        servico = kwargs.get("servico")
        try:
            arquivo = os.path.join("Projeto_Migracao", self.sistema, "Pre_Validacao", f"{servico['nome']}.sql")
            with open(arquivo, 'r', encoding='utf-8') as arquivo:
                script = arquivo.read()
                script_formatado = sqlparse.format(script, reindent=True, keyword_case='upper')
            cursor_destino = criar_cursor('destino')
            cursor_destino.execute(script_formatado)
            self.salvar_retorno_sql_em_txt(cursor_destino.fetchall(), f"resultado_pre_validacao_{servico['nome']}.txt")
            return True
        
        
        
        except Exception as e:
            print(f"Erro ao executar a pré-validação: {e}")
            return False
        finally:
            cursor_destino.close()