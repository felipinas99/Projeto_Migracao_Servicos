def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "aliquotasSimplesNac": {
                "dtInicialVigencia": item.data_inicial_vigencia,
                "dtFinalVigencia": item.data_final_vigencia,
                "tipoTabela": item.tipo_tabela
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno