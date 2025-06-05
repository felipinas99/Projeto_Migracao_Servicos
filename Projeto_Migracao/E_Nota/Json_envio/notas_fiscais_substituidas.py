def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "notas-fiscais-substituidas": {
                "dhSubstituicao": item.data_hora_substituicao,
                "idsNotasFiscaisSubstituidas": [
                    item.notas_substituidas_cloud_id   
                ],
                "idsNotasFiscaisSubstitutas": [
                    item.notas_substitutas_cloud_id
                ],
                "motivoSubstituicao": item.motivo_substituicao,
                "nroProtocolo": item.nro_protocolo,
                "idContribuintes": item.contribuinte_cloud_id
        }
        }

        if funcao == 'Atualizar':
            dado["notas-fiscais-substituidas"]["idGerado"] = {"id": item.id_gerado }
        retorno.append(dado)
    return retorno