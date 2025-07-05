import locale
from ttkbootstrap.constants import BOTTOM, CENTER, LEFT, X, RIGHT
import ttkbootstrap as ttk ,os, sys
from Projeto_Migracao.visual.Funcoes_app import abrir_deletar_registros, atualizar_tabela_periodicamente, criar_rotulo, cria_frame_tabela, abrir_configurar_banco, abrir_parametros
from Projeto_Migracao.utilitario.processamento_controller import ProcessamentoController
from Projeto_Migracao.utilitario.Funcoes import busca_parametro, ler_pasta_config_json, ler_servicos_json
from Projeto_Migracao.visual.botoes import Botoes
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path:
    sys.path.append(base_dir)

processamento_controller = ProcessamentoController()
processamento_controller.start()

try:
    servicos  = []
    if processamento_controller.motor_construido is True:
        sistema = busca_parametro('Sistema')
    caminho = f'Projeto_Migracao\\{sistema}'
    pasta_config = ler_pasta_config_json(caminho)
    servicos = ler_servicos_json(pasta_config)
except Exception as e:
    print(f"Erro ao ler o arquivo de configuração: {e}")



def main():
    janela = ttk.Window(themename="darkly")
    janela.geometry("1200x800")

    menu_bar = ttk.Menu(janela)
    janela.config(menu=menu_bar)

    file_menu_config = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuracoes", menu=file_menu_config)
    file_menu_dados = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Dados", menu=file_menu_dados)
    file_menu_config.add_command(label="Bancos", command=abrir_configurar_banco)
    file_menu_config.add_separator()
    file_menu_config.add_command(label="Parâmetros", command=lambda:abrir_parametros(processamento_controller))
    file_menu_config.add_separator()
    file_menu_config.add_command(label="Deletar Registro", command=abrir_deletar_registros)
    file_menu_config.add_separator()
    file_menu_config.add_command(label="Sair", command=janela.quit)
    file_menu_dados.add_command(label="lotes", command=cria_frame_tabela)

    criar_rotulo(janela, "Serviços Disponíveis:", 12)

    # Frame dos servicos (esquerda)
    frame_servicos = ttk.Frame(janela)
    frame_servicos.pack(side=LEFT, fill='y', expand=False, padx=0, pady=10, ipadx=10, ipady=0)
    canvas = ttk.Canvas(frame_servicos, width=550)
    scrollbar = ttk.Scrollbar(frame_servicos, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for servico in servicos:
        frame_servico = ttk.Frame(scrollable_frame, padding="10 20 0 0")
        frame_servico.pack(pady=0, padx=0, fill=X)
        label_servico = ttk.Label(frame_servico, text=servico["nome"], font=("Helvetica", 10))
        label_servico.pack(anchor="w", pady=(0, 2))
        frame_botoes = ttk.Frame(frame_servico)
        frame_botoes.pack(anchor="w", fill="x")
        botao = Botoes()
        botao.criar_botao_servico(frame_botoes, 'Extrair', servico, caminho, processamento_controller.iniciar_extracao)
        botao.criar_botao_servico(frame_botoes, 'Resgate', servico, caminho, processamento_controller.iniciar_resgate)
        botao.criar_botao_servico(frame_botoes, 'Enviar', servico, caminho, processamento_controller.iniciar_envios)
        botao.criar_botao_servico(frame_botoes, 'Atualizar', servico, caminho, processamento_controller.iniciar_atualizacao)
        # criar_botao_servico(frame_botoes, 'Deletar', servico, caminho, iniciar_delete)

    # Mini tabela do lado direito
    frame_tabela = ttk.Frame(janela, height=90)
    frame_tabela.pack(side=RIGHT,  anchor="n",expand=False, padx=10, pady=10)
    label_tabela = ttk.Label(frame_tabela, text="Lotes", font=("Helvetica", 12))
    label_tabela.pack(anchor="center", pady=(0, 5))
    columns = ("Lotes",  "Metodo", "Tipo Registro","Total")
    tree = ttk.Treeview(frame_tabela, columns=columns, show="headings", height=10)
    tree.column("Lotes", width=180, anchor="center")
    tree.column("Metodo", width=60, anchor="center")
    tree.column("Tipo Registro", width=150, anchor="center")
    tree.column("Total", width=60, anchor="center")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)
    atualizar_tabela_periodicamente(tree, processamento_controller.motor_construido)

    # def acao_status_postagem():
    #     processamento_controller.status_postagem = True
    #     status_label.config(text="Motor ligado", bootstyle="success")

    # # Adicione o botão e um label para feedback visual
    # frame_status = ttk.Frame(janela)
    # frame_status.pack(side="top", pady=10)

    # botao_status = ttk.Button(frame_status, text="Status Postagem", command=acao_status_postagem, bootstyle="info")
    # botao_status.pack(side="left", padx=5)

    # status_label = ttk.Label(frame_status, text="Status: Aguardando", font=("Helvetica", 10))
    # status_label.pack(side="left", padx=10)
    

    rodape = ttk.Label(janela, text="Projeto Migração de dados", font=("Helvetica", 10), anchor=CENTER)
    rodape.pack(side=BOTTOM, fill=X, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()