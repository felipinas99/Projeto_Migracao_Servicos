import ttkbootstrap as ttk 
from Funcoes_app import *
from utilitario.Funcoes import ler_pasta_config_json, ler_servicos_json, iniciar_delete, iniciar_atualizacao, iniciar_envios, iniciar_extracao
import json

config = ler_pasta_config_json(r'Projeto_Migracao\Servicos_Padrao')


servicos = ler_servicos_json(config)

def main():
    # Cria a janela principal com um tema moderno
    janela = ttk.Window(themename="darkly")

    # Adiciona a barra de menu
    menu_bar = ttk.Menu(janela)
    janela.config(menu=menu_bar)

    #Menus Principais
    file_menu = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuracoes", menu=file_menu)

    #Menu do banco
    file_menu.add_command(label="Bancos", command=abrir_configurar_banco)
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=janela.quit)

    # Título da janela principal
    criar_rotulo(janela, "Serviços Disponíveis:", 16)

    # Frame dos servicos
    frame_servicos = ttk.Frame(janela)
    frame_servicos.pack(side=LEFT, fill=BOTH, expand=True)
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
        frame_servico = ttk.Frame(scrollable_frame, padding="10 10 10 10")
        frame_servico.pack(pady=15, padx=10, fill=X)

        label_servico = ttk.Label(frame_servico, text=servico, font=("Helvetica", 14))
        label_servico.pack(side=LEFT, padx=10)

        criar_botao_servico(frame_servico, 'Extrair', servico, iniciar_extracao)
        criar_botao_servico(frame_servico, 'Enviar', servico, iniciar_envios)
        criar_botao_servico(frame_servico, 'Atualizar', servico, iniciar_atualizacao)
        criar_botao_servico(frame_servico, 'Deletar', servico, iniciar_delete)


    # Cria o frame de dados dentro da janela principal
    cria_frame_tabela(janela)

    # Adiciona o campo "Lotes em Processamento"
    label_lotes = ttk.Label(janela, text="Lotes em Processamento: 0", font=("Helvetica", 14))
    label_lotes.pack(pady=10)
    atualizar_lotes(label_lotes)
    
    # frase no rodapé
    rodape = ttk.Label(janela, text="Projeto Migração de dados", font=("Helvetica", 10), anchor=CENTER)
    rodape.pack(side=BOTTOM, fill=X, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()