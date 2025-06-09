import time
import ttkbootstrap as ttk 
from ttkbootstrap.constants import TRUE
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
import os, json
import threading

from Projeto_Migracao.utilitario.Funcoes import criar_cursor

config_file = "Projeto_Migracao/config_banco.json"



def criar_rotulo(janela, texto, tamanho=14):
    rotulo = ttk.Label(janela, text=texto, font=("Helvetica", tamanho))
    rotulo.pack(pady=5)

def criar_botao(janela, texto, comando):
    botao = ttk.Button(janela, text=texto, command=comando)
    botao.pack(pady=5)

def criar_entrada(janela, tamanho=14, largura = 50):
    entrada = ttk.Entry(janela, font=("Helvetica", tamanho), width=largura)
    entrada.pack(pady=5)
    return entrada 

def mostrar_mensagem(entrada):
    texto = entrada.get()
    Messagebox.show_info(f"Você digitou: {texto}", title="Mensagem")

def cria_janela(titulo):
    janela = ttk.Window(themename="cosmo")  # Usando ttkbootstrap para criar a janela
    janela.title(titulo)
    janela.state('zoomed')  # Maximiza a janela
    return janela



def cria_frame_tabela():
    configurar_banco_janela = ttk.Toplevel()  # Usando ttkbootstrap para criar a janela
    configurar_banco_janela.title("Configurar Banco")
    configurar_banco_janela.geometry("900x700+0+0")

    coldata = [
    {"text": "ID", "stretch": TRUE},
    {"text": "Nome", "stretch": TRUE},
    {"text": "Idade", "stretch": TRUE},
]

    rowdata = [
        ("1", "João", 28),
        ("2", "Maria", 34),
        ("3", "Pedro", 45),
    ]

    tabela = Tableview(
        master=configurar_banco_janela,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        pagesize = 30,
        autofit=True,
        bootstyle="info",
    )
    tabela.pack( fill="both", expand=True)


def salvar_configuracao(campos,campos_origem, campos_destino):
    config = {
        "origem": {campo: campos_origem[i].get() for i, campo in enumerate(campos)},
        "destino": {campo: campos_destino[i].get() for i, campo in enumerate(campos)}
    }

    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def carregar_configuracao():
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f) 
                campos_origem = [config["origem"].get(chave, "") for chave in ["DRIVER", "UID", "PWD", "DATABASE", "SERVER", "PORT", "DSN", "APP"]]
                campos_destino = [config["destino"].get(chave, "") for chave in ["DRIVER", "UID", "PWD", "DATABASE", "SERVER", "PORT", "DSN", "APP"]]
                return campos_origem + campos_destino
        except json.JSONDecodeError as e:
            print(f"Erro ao carregar configuração: {e}")
            return []
    return []

def carregar_dados_tabela(tabela):
    cursor = criar_cursor('destino')
    cursor.execute(f'select * from motor.{tabela}')
    dados = cursor.fetchall()
    return dados

def abrir_configurar_banco():
    configurar_banco_janela = ttk.Toplevel()  # Usando ttkbootstrap para criar a janela
    configurar_banco_janela.title("Configurar Banco")
    configurar_banco_janela.geometry("900x700+0+0")

    frame_origem = ttk.Frame(configurar_banco_janela, padding="5 5 5 5")
    frame_origem.pack(side="left", fill="both", expand=True)

    frame_destino = ttk.Frame(configurar_banco_janela, padding="5 5 5 5")
    frame_destino.pack(side="right", fill="both", expand=True)

    campos = ["DRIVER", "UID", "PWD", "DATABASE", "SERVER", "PORT", "DSN", "APP"]
    entradas_origem = []
    entradas_destino = []

    configuracoes = carregar_configuracao()

    for frame, titulo, entradas in [(frame_origem, "Origem", entradas_origem), (frame_destino, "Destino", entradas_destino)]:
        criar_rotulo(frame, f"Configurar Banco de Dados ({titulo})", 14)
        for i, campo in enumerate(campos):
            criar_rotulo(frame, f"{campo}:", 14)
            entrada = criar_entrada(frame, 14)
            if configuracoes:
                entrada.insert(0, configuracoes.pop(0))
            entradas.append(entrada)

    botao_salvar = ttk.Button(configurar_banco_janela, text="Salvar", command=lambda: salvar_configuracao(campos,entradas_origem, entradas_destino))
    botao_salvar.pack(pady=10)
    
def abrir_parametros():
    configurar_banco_janela = ttk.Toplevel()
    configurar_banco_janela.title("Configurar Parametros")
    configurar_banco_janela.geometry("900x700+0+0")

    frame = ttk.Frame(configurar_banco_janela, padding="5 5 5 5")
    frame.pack(side="left", fill="both", expand=True)

    campos = ["Token","Sistema","Concorrente","Url_Base","Url_Lote"]
    parametros = []

    configuracoes = carregar_dados_tabela('parametros')
    configuracoes_dict = {linha[1]: linha[2] for linha in configuracoes}  # Supondo que a estrutura seja (id, tipo_parametro, valor)

    for frame, titulo, entradas in [(frame, "Parametros", parametros)]:
        criar_rotulo(frame, f"Configurar Parâmetros ({titulo})", 14)
        for campo in campos:
            criar_rotulo(frame, f"{campo}:", 14)
            entrada = criar_entrada(frame, 14)
            # Insere o valor correspondente ao campo, se existir no dicionário
            if campo in configuracoes_dict:
                entrada.insert(0, configuracoes_dict[campo])
            entradas.append(entrada)

    def salvar_parametros():
        for i, campo in enumerate(campos):
            valor = parametros[i].get()  # Obtém o valor do campo
            try:
                cursor = criar_cursor('destino')
                # Atualiza ou insere o valor no banco de dados
                cursor.execute(
                    "INSERT INTO motor.parametros (tipo_parametro, valor) VALUES (?, ?) "
                    "ON CONFLICT (tipo_parametro) DO UPDATE SET valor = EXCLUDED.valor",
                    (campo, valor)
                )       
                cursor.execute("commit")
                print(f"Parâmetro '{campo}' salvo com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar o parâmetro '{campo}': {e}")

    # Botão para salvar os dados
    botao_salvar = ttk.Button(configurar_banco_janela, text="Salvar", command=salvar_parametros)
    botao_salvar.pack(pady=10)

def abrir_deletar_registros():
    configurar_banco_janela = ttk.Toplevel()
    configurar_banco_janela.title("Deletar Registros")
    configurar_banco_janela.geometry("900x700+0+0")

    frame = ttk.Frame(configurar_banco_janela, padding="5 5 5 5")
    frame.pack(side="left", fill="both", expand=True)

    campos = ["Tipo","SQL","Tabela"]
    parametros = []

    for frame, titulo, entradas in [(frame, "Parametros", parametros)]:
        criar_rotulo(frame, f"Configurar Parâmetros ({titulo})", 14)
        for campo in campos:
            criar_rotulo(frame, f"{campo}:", 14)
            entrada = criar_entrada(frame, 14)
            entradas.append(entrada)



def criar_botao_servico(frame, funcao, servico, caminho, acao):
    botao = ttk.Button(
        frame,
        text=funcao,
        command=lambda: acao_com_cor(botao, servico=servico, funcao=funcao, caminho=caminho, acao=acao)
    )
    botao.pack(side="left", padx=5, pady=2)


def acao_com_cor(botao, **kwargs):
    servico = kwargs.get("servico")
    funcao = kwargs.get("funcao")
    acao = kwargs.get("acao")

    botao.config(state="disabled", text=f"Processando {funcao}...")

    def run_acao():
        retorno = acao(servico=servico, funcao=funcao)
        # Atualize o botão na thread principal
        botao.after(0, lambda: atualizar_botao(botao, funcao, retorno))

    def atualizar_botao(botao, funcao, retorno):
        if retorno == True:
            botao.config(state="normal", text="Sucesso " + funcao, bootstyle="success")
        else:
            botao.config(state="normal", text="Falha " + funcao, bootstyle="danger")
        botao.after(3000, lambda: botao.config(text=funcao, bootstyle="primary"))

    threading.Thread(target=run_acao).start()




def atualizar_tabela_itens(tree, cursor=None):
    try:
        if cursor is None:
            cursor = criar_cursor('destino')
            # Armazene o cursor no widget para reuso
            tree.cursor = cursor
        else:
            cursor = tree.cursor
    except Exception as e:
        return  # Não continue se não conseguir o cursor

    try:
        cursor.execute('''
            select 'Pendentes Envio' as descricao , metodo::text,tipo_registro,count(*) from motor.lotes_pendentes_envio lpe  group by 1,2,3
union 
select 'Pendentes Processamento' as descricao,'',tipo_registro,count(*) from motor.lotes_pendentes_processamento lpp group by 1,2,3 
union 
select 'Pendentes Resgate' as descricao,'',tipo_registro,count(*) from motor.lotes_pendentes_resgate lpr group by 1,2,3
order by 1,2,3,4
        ''')
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert('', 'end', values=(row.descricao, row.metodo,row.tipo_registro, row.count))
        # Atualiza novamente em 5 segundos, reutilizando o mesmo cursor
        tree.after(2000, lambda: atualizar_tabela_itens(tree, cursor))
    except Exception as e:
        pass

def atualizar_tabela_periodicamente(tree, intervalo=5):
    def worker():
        while True:
            # Consulta ao banco em thread separada
            try:
                from Projeto_Migracao.utilitario.Funcoes import criar_cursor
                cursor = criar_cursor('destino')
                cursor.execute('''
                    select 'Pendentes Envio' as descricao , metodo::text,tipo_registro,count(*) from motor.lotes_pendentes_envio lpe  group by 1,2,3
                    union 
                    select 'Pendentes Processamento' as descricao,'',tipo_registro,count(*) from motor.lotes_pendentes_processamento lpp group by 1,2,3 
                    union 
                    select 'Pendentes Resgate' as descricao,'',tipo_registro,count(*) from motor.lotes_pendentes_resgate lpr group by 1,2,3
                    order by 1,2,3,4
                ''')
                rows = cursor.fetchall()
                cursor.close()
            except Exception as e:
                rows = []

            # Atualiza a Treeview na thread principal
            def atualizar_treeview():
                tree.delete(*tree.get_children())
                for row in rows:
                    tree.insert('', 'end', values=(row.descricao, row.metodo, row.tipo_registro, row.count))
            tree.after(0, atualizar_treeview)
            time.sleep(intervalo)
    threading.Thread(target=worker, daemon=True).start()