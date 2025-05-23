import threading
from ttkbootstrap.constants import BOTTOM, CENTER, LEFT, X
import ttkbootstrap as ttk ,os, sys
from Funcoes_app import criar_rotulo, criar_botao_servico, cria_frame_tabela, abrir_configurar_banco, abrir_parametros
from utilitario.Funcoes import busca_parametro, iniciar_resgate, ler_pasta_config_json, ler_servicos_json, iniciar_delete, iniciar_atualizacao, iniciar_envios, iniciar_extracao, postagem, get_lotes, atualiza_retorno_lote_itens

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path:
    sys.path.append(base_dir)



threading.Thread(target=postagem).start()
threading.Thread(target=get_lotes).start()
threading.Thread(target=atualiza_retorno_lote_itens).start()


try:
    servicos  = []
    sistema = busca_parametro('Sistema')
    caminho = f'Projeto_Migracao\\{sistema}'
    pasta_config = ler_pasta_config_json(caminho)
    servicos = ler_servicos_json(pasta_config)
except Exception as e:
    print(f"Erro ao ler o arquivo de configuração: {e}")

def main():
    # Cria a janela principal com um tema moderno
    janela = ttk.Window(themename="darkly")
    janela.geometry("1200x800")

    # Adiciona a barra de menu
    menu_bar = ttk.Menu(janela)
    janela.config(menu=menu_bar)

    #Menus Principais
    file_menu_config = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuracoes", menu=file_menu_config)

    file_menu_dados = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Dados", menu=file_menu_dados)

    #Menu do banco
    file_menu_config.add_command(label="Bancos", command=abrir_configurar_banco)
    file_menu_config.add_separator()
    file_menu_config.add_command(label="Parâmetros", command=abrir_parametros)
    file_menu_config.add_separator()
    file_menu_config.add_command(label="Sair", command=janela.quit)

    #Menu do dados
    file_menu_dados.add_command(label="lotes", command=cria_frame_tabela)

    # Título da janela principal
    criar_rotulo(janela, "Serviços Disponíveis:", 12)

    # Frame dos servicos
    frame_servicos = ttk.Frame(janela)
    frame_servicos.pack(side=LEFT, fill='y', expand=False, padx=0, pady=10, ipadx=10, ipady=0)
    canvas = ttk.Canvas(frame_servicos)
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

    # Lista os servicos do config.json e cria os botões atribuindo suas funcoes
    for servico in servicos:
        frame_servico = ttk.Frame(scrollable_frame, padding="10 15 0 0")
        frame_servico.pack(pady=0, padx=0, fill=X)

        label_servico = ttk.Label(frame_servico, text=servico["nome"], font=("Helvetica", 10))
        label_servico.pack(side=LEFT, padx=0)

        criar_botao_servico(frame_servico, 'Extrair', servico, caminho, iniciar_extracao)
        criar_botao_servico(frame_servico, 'Resgate', servico, caminho, iniciar_resgate)
        criar_botao_servico(frame_servico, 'Enviar', servico,  caminho, iniciar_envios)
        criar_botao_servico(frame_servico, 'Atualizar', servico, caminho, iniciar_atualizacao)
        criar_botao_servico(frame_servico, 'Deletar', servico,  caminho, iniciar_delete)
    
    # frase no rodapé
    rodape = ttk.Label(janela, text="Projeto Migração de dados", font=("Helvetica", 10), anchor=CENTER)
    rodape.pack(side=BOTTOM, fill=X, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()