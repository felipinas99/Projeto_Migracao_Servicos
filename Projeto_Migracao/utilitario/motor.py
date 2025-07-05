import os

import sqlparse

from Projeto_Migracao.utilitario.Funcoes import busca_parametro, criar_cursor, execute_sql_extracao

class Motor:
    def __init__(self):
        self.motor_construido: bool = False
        self.token: str | None = None
        self.url_envio: str | None = None
        self.url_lote: str | None = None
        self.sistema: str | None = None
        self.concorrente: str | None = None
        # Caminho absoluto para o arquivo tabelas_padrao.sql na pasta atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.tabelas_padrao_path = os.path.join(current_dir, "tabelas_padrao.sql")

    def recarregar_informações(self):
        self.token = busca_parametro('Token')
        self.url_envio = busca_parametro('Url_Base')
        self.url_lote = busca_parametro('Url_Lote')
        self.sistema = busca_parametro('Sistema')
        self.concorrente = busca_parametro('Concorrente')

        print("motor recarregado com sucesso.")

        if not all([self.token, self.url_envio, self.url_lote, self.sistema, self.concorrente]):
            raise ValueError("Parâmetros de configuração incompletos.")

    def executar_tabelas_padrao(self, cursor):
        """
        Executa o script SQL do arquivo tabelas_padrao.sql usando o cursor fornecido.
        """
        if not os.path.exists(self.tabelas_padrao_path):
            print(f"Arquivo não encontrado: {self.tabelas_padrao_path}")
            return False

        with open(self.tabelas_padrao_path, "r", encoding="utf-8") as f:
            script = f.read()
        try:
            cursor.execute(script)
            cursor.execute("commit;")
            print("Script tabelas_padrao.sql executado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao executar tabelas_padrao.sql: {e}")
            return False

    def atualiza_dependencias_tabela_controle(self,servico,sistema):
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
            print(f"Erro ao executar a atualizacao de dependencias de tabelas: {e}")
            return False
        finally:
            cursor_destino.close()


    def checa_motor(self):
        try:
            cursor_motor = criar_cursor('destino')
            cursor_motor.execute('SELECT * FROM motor.controle_lotes limit 1')
            cursor_motor.execute('SELECT * FROM motor.lotes_pendentes_resgate')
            cursor_motor.execute('SELECT * FROM motor.lotes_pendentes_processamento')
            cursor_motor.execute('SELECT * FROM motor.lotes_pendentes_envio')
            self.motor_construido = True
        except Exception as e:
            print(f"Erro ao checar motor: {e}")
            self.motor_construido = False