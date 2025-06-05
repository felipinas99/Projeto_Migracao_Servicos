def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
             "notas-fiscais-cancelamento": {
                "idNota": item.nota_fiscal_cloud_id,
                "nroProtocolo": item.nro_prtocolo,
                "dhCancelamento": item.data_hora_cancelamento,
                "motivo": item.motivo,
                "processo": item.processo,
                "idContribuintes": item.contribuinte_cloud_id
            }
        }

        if funcao == 'Atualizar':
            dado["notas-fiscais-cancelamento"]["idGerado"]["id"] = dado.id_gerado
        retorno.append(dado)
    return retorno