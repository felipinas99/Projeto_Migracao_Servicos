def montar(lista):
    for item in lista:
        dado = {
            "idIntegracao": item["id"],
            "conteudo": {
                "nome": item["nome"]
            }
        }
        yield dado