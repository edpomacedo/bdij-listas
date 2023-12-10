import os
import requests
from requests_oauthlib import OAuth1
from config import MEDIAWIKI_CONFIG
import hashlib
from bs4 import BeautifulSoup
from tabulate import tabulate

# Solicitar a URL da fonte no terminal
url_fonte = input("Digite a URL da fonte: ")

# Realiza a requisição HTTP para obter o conteúdo da página
response = requests.get(url_fonte)

# Verificar o status da resposta
if response.status_code == 200:
    print('Requisição bem-sucedida. Continuando...')
else:
    print(f'Erro na requisição HTTP. Código de status: {response.status_code}')
    exit()

# Utiliza BeautifulSoup para analisar o HTML da página
soup = BeautifulSoup(response.text, 'html.parser')

# Encontra a tag <pre> que contém a consulta SPARQL
pre_tag = soup.find('pre')

# Verifica se a tag <pre> foi encontrada
if pre_tag:
    # Recupera o texto contido na tag <pre>
    consulta_sparql = pre_tag.text

    # Parâmetros da requisição SPARQL
    parametros = {
        "query": consulta_sparql,
        "format": "json"  # ou o formato desejado para os resultados
    }

    # Envio da requisição POST para o endpoint SPARQL
    response_sparql = requests.post(MEDIAWIKI_CONFIG.get('endpoint_url', ''), data=parametros)

    # Verificação do status da resposta
    if response_sparql.status_code == 200:
        # Obtenção dos resultados
        resultados = response_sparql.json()

        # Transforma os resultados em uma lista de dicionários
        dados_tabela = []
        for resultado in resultados["results"]["bindings"]:
            linha = {chave: valor['value'] for chave, valor in resultado.items()}
            dados_tabela.append(linha)

        # Perguntar ao usuário o tipo de resultado
        print("Selecione o tipo de resultado:")
        print("1. Lexeme")
        print("2. Item")

        # Obter a resposta do usuário
        opcao = input("Digite o número correspondente à opção desejada: ")

        # Verificar a opção escolhida e realizar tratamento específico
        if opcao == "1":
            tipo_resultado = "Lexeme"
            for linha in dados_tabela:
                for chave in linha:
                    if isinstance(linha[chave], str) and linha[chave].startswith("https://web.bdij.com.br/entity/"):
                        lexeme_id = linha[chave][len("https://web.bdij.com.br/entity/"):]
                        reference_id = lexeme_id.replace("-", "#")  # Substituir "-" por "#"
                        # Substituir e formatar para [[Lexeme:L1|L1]]
                        linha[chave] = f"[[Lexeme:{reference_id}|{lexeme_id}]]"
        elif opcao == "2":
            tipo_resultado = "Item"
            for linha in dados_tabela:
                for chave in linha:
                    if isinstance(linha[chave], str) and linha[chave].startswith("https://web.bdij.com.br/entity/"):
                        item_id = linha[chave][len("https://web.bdij.com.br/entity/"):]
                        reference_id = item_id.replace("-", "#")  # Substituir "-" por "#"
                        # Substituir e formatar para [[Item:Q1|Q1]]
                        linha[chave] = f"[[Item:{reference_id}|{item_id}]]"
        else:
            print("Opção inválida. Saindo do programa.")
            exit()

        # Adiciona os cabeçalhos e contagem de resultados
        cabeçalhos = dados_tabela[0].keys()
        contagem_resultados = len(dados_tabela)

        # Construir o nome do arquivo usando um hash
        hash_nome_arquivo = hashlib.md5(consulta_sparql.encode('utf-8')).hexdigest()
        caminho_arquivo = os.path.join('tables', f'{hash_nome_arquivo}.txt')

        # Adiciona os cabeçalhos à tabela wikitext
        tabela_wikitext = f"{{| class=\"wikitable sortable\" style=\"width:100%;\"\n|+ Número de resultados: {contagem_resultados}\n|-"
        tabela_wikitext += f"\n! {' !! '.join(cabeçalhos)}\n"

        # Adiciona as linhas da tabela
        for linha in dados_tabela:
            tabela_wikitext += "|-\n"
            tabela_wikitext += f"| {' || '.join(str(linha[coluna]) for coluna in cabeçalhos)}\n"

        # Finaliza a tabela wikitext
        tabela_wikitext += "|}\n"

        # Salvar o resultado no arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(tabela_wikitext)

        print(f"Resultado salvo em: {caminho_arquivo}")

        # Solicitar o nome da página de destino no terminal
        nome_pagina_destino = input("Digite o nome da página de destino: ")

        # Configuração do cliente OAuth1
        oauth = OAuth1(
            MEDIAWIKI_CONFIG['consumer_key'],
            client_secret=MEDIAWIKI_CONFIG['consumer_secret'],
            resource_owner_key=MEDIAWIKI_CONFIG['access_token'],
            resource_owner_secret=MEDIAWIKI_CONFIG['access_token_secret']
        )

        # URL para verificar se a página existe
        api_page_url = MEDIAWIKI_CONFIG['api_url'] + f'?action=query&titles={nome_pagina_destino}&format=json'
        response_page = requests.get(url=api_page_url, auth=oauth)

        if response_page.status_code == 200:
            pages = response_page.json()['query']['pages']
            page_exists = list(pages.keys())[0] != "-1"

            if page_exists:
                print(f"A página {nome_pagina_destino} já existe. A edição não foi realizada.")
            else:
                # Obter o token de edição
                api_token_url = MEDIAWIKI_CONFIG['api_url'] + '?action=query&meta=tokens&type=csrf&format=json'
                response_token = requests.get(url=api_token_url, auth=oauth)

                if response_token.status_code == 200:
                    token_edicao = response_token.json()['query']['tokens']['csrftoken']

                    # Parâmetros para a edição da página, incluindo o token de edição
                    params = {
                        'action': 'edit',
                        'title': f'Project:{nome_pagina_destino}',
                        'text': tabela_wikitext,
                        'contentformat': 'text/x-wiki',
                        'contentmodel': 'wikitext',
                        'minor': 'true',
                        'recreate': 'true',
                        'summary': '',
                        'format': 'json',
                        'token': token_edicao
                    }

                    # Requisição para editar a página
                    response_edit = requests.post(url=MEDIAWIKI_CONFIG['api_url'], auth=oauth, data=params)

                    if response_edit.status_code == 200:
                        print(f"Postagem realizada com sucesso na página: Project:{nome_pagina_destino}")
                    else:
                        print(f"Erro ao postar para a página Project:{nome_pagina_destino}. Status: {response_edit.status_code}, Resposta: {response_edit.text}")
                else:
                    print(f"Erro ao obter o token de edição. Status: {response_token.status_code}, Resposta: {response_token.text}")
        else:
            print(f'Erro ao verificar se a página existe. Status: {response_page.status_code}, Resposta: {response_page.text}')

    else:
        print(f"Falha na requisição SPARQL. Código de status: {response_sparql.status_code}")

else:
    print("Tag <pre> não encontrada na página.")
