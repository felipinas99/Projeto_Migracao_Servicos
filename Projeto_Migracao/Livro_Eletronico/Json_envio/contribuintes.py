def montar(lista, funcao):
    retorno = []
    for item in lista:
        dado = {
            "idIntegracao": item.id,
            "contribuintes": {
                "iPessoas": item.pessoa_cloud_id,
                "iContadores": item.contador_cloud_id,
                "itipos": item.tipo_cloud_id,
                "ibancos": item.banco_cloud_id,
                "iListasServicos": item.lista_servico_cloud_id,
                "enquadramento": item.enquadramento,
                "tipoContribuinte": item.tipo_contribuinte,
                "dtAdesaoNota": item.data_adesao_nota,
                "tipoPessoa": item.tipo_pessoa,
                "cpfCnpj": item.cpf_cnpj,
                "optanteSn": item.optante_sn,
                "escrituraDfp": item.escritura_dfp,
                "escrituraDft": item.escritura_dft,
                "permiteDeducao": item.permite_deducao,
                "declaraConjugada": item.declara_conjugada,
                "descontadoPrefeitura": item.descontado_prefeitura,
                "permiteTaxasEspeciais": item.permite_taxas_especiais,
                "isentoTaxaExpediente": item.isento_taxa_expediente,
                "possuiPendencias": item.possui_pendencias,
                "permiteGerarDeclPorDoc": item.permite_gerar_decl_por_documento,
                "dtAbertura": item.data_abertura
            }
        }

        if funcao == 'Atualizar':
            dado["bairro"]["idGerado"] = {"id": item.id_gerado}
        retorno.append(dado)
    return retorno