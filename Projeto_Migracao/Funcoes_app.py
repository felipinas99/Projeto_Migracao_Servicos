import ttkbootstrap as ttk  # Certifique-se de usar ttkbootstrap
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import *
from ttkbootstrap.tableview import *
import random
import os, json, psycopg2
import threading

config_file = "config_banco.json"

def criar_rotulo(janela, texto, tamanho=14):
    rotulo = ttk.Label(janela, text=texto, font=("Helvetica", tamanho))
    rotulo.pack(pady=5)

def criar_botao(janela, texto, comando):
    botao = ttk.Button(janela, text=texto, command=comando)
    botao.pack(pady=5)

def criar_entrada(janela, tamanho=14):
    entrada = ttk.Entry(janela, font=("Helvetica", tamanho))
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

def obter_dados():
    # Função que retorna uma lista de dados com 4 colunas
    return [[random.randint(1, 100) for _ in range(4)] for _ in range(100)]

# def atualizar_tabela_treeview(treeview):
#     for item in treeview.get_children():
#         treeview.delete(item)
#     dados = obter_dados()[:100]  # Limita a 100 itens
#     for linha in dados:
#         treeview.insert("", "end", values=linha)
#     treeview.after(2000, atualizar_tabela, treeview)  # Atualiza a cada 2 segundos

# def criar_frame_dados_treeview(janela):
#     frame_dados = ttk.Frame(janela, padding="10 10 10 10")
#     frame_dados.pack(side="right", fill="both", expand=True)

#     colunas = ("Coluna1", "Coluna2", "Coluna3", "Coluna4")
#     treeview = ttk.Treeview(frame_dados, columns=colunas, show="headings")
#     for col in colunas:
#         treeview.heading(col, text=col)
#         treeview.column(col, width=100)
#     treeview.pack(side="left", fill="both", expand=True)

#     scrollbar = ttk.Scrollbar(frame_dados, orient="vertical", command=treeview.yview)
#     treeview.configure(yscrollcommand=scrollbar.set)
#     scrollbar.pack(side="right", fill="y")

#     atualizar_tabela_treeview(treeview)

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


def atualizar_lotes(label):
    # Função que simula a atualização dos lotes em processamento
    lotes = random.randint(1, 50)
    label.config(text=f"Lotes em Processamento: {lotes}")
    label.after(2000, atualizar_lotes, label)  # Atualiza a cada 2 segundos

def salvar_configuracao(campos,campos_origem, campos_destino):
    config = {
        "origem": {campo: campos_origem[i].get() for i, campo in enumerate(campos)},
        "destino": {campo: campos_destino[i].get() for i, campo in enumerate(campos)}
    }

    for tipo in ["destino"]:
        conf = config[tipo]
        try:
            # Tenta conectar ao banco informado
            conn = psycopg2.connect(
                dbname="postgres",  # Conecta ao banco padrão para criar outro
                user=conf["UID"],
                password=conf["PWD"],
                host=conf["SERVER"],
                port=conf["PORT"]
            )
            conn.autocommit = True
            cur = conn.cursor()

            # Verifica se o banco já existe
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (conf["DATABASE"],))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE "{conf["DATABASE"]}"')
                print(f'Banco "{conf["DATABASE"]}" criado para {tipo}.')
            else:
                print(f'Banco "{conf["DATABASE"]}" já existe para {tipo}.')

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Erro ao validar/criar banco {tipo}: {e}")

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


def criar_botao_servico(frame, funcao, servico, caminho, acao):
    botao = ttk.Button(
        frame,
        text=funcao,
        command=lambda: acao_com_cor(botao, servico=servico, funcao=funcao, caminho = caminho, acao=acao)
    )
    botao.pack(side=LEFT, padx=5)


def acao_com_cor(botao, **kwargs):
    servico = kwargs.get("servico")
    funcao = kwargs.get("funcao")
    acao = kwargs.get("acao")
    caminho = kwargs.get("caminho")

    botao.config(state="disabled", text=f"Processando {funcao}...")

    def run_acao():
        retorno = acao(servico, caminho, funcao)
        # Atualize o botão na thread principal
        botao.after(0, lambda: atualizar_botao(botao, funcao, retorno))

    def atualizar_botao(botao, funcao, retorno):
        if retorno == True:
            botao.config(state="normal", text="Sucesso " + funcao, bootstyle="success")
        else:
            botao.config(state="normal", text="Falha " + funcao, bootstyle="danger")
        botao.after(3000, lambda: botao.config(text=funcao, bootstyle="primary"))

    threading.Thread(target=run_acao).start()




