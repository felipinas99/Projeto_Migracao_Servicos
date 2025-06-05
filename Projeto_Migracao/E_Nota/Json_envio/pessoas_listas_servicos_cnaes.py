def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "pessoas-listas-servicos-cnaes": {
                "aliquota": item.aliquota,
                "idPessoa": item.pessoa_cloud_id,
                "codigoListaServicoEntidade": item.codigo_lista_servico_entidade
            }
        }
        if item.codigo_cnae != None:
            dado["pessoas-listas-servicos-cnaes"]["codigoCnae"] = item.codigo_cnae

        if funcao == 'Atualizar':
            dado["pessoas-listas-servicos-cnaes"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno