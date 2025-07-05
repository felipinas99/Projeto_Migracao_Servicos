import threading
import ttkbootstrap as ttk

class Botoes:
    def __init__(self):
        pass

    def criar_botao_servico(self, frame, funcao, servico, caminho, acao):
        botao = ttk.Button(
            frame,
            text=funcao,
            command=lambda: self.acao_com_cor(botao, servico=servico, funcao=funcao, caminho=caminho, acao=acao)
        )
        botao.pack(side="left", padx=5, pady=2)

    def acao_com_cor(self, botao, **kwargs):
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