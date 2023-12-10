import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import hashlib
import os

# URL do endpoint SPARQL
endpoint_url = "https://web.bdij.com.br/query/sparql"

# Realiza a requisição HTTP para obter o conteúdo da página
response = requests.get("https://web.bdij.com.br/wiki/Project_talk:Minist%C3%A9rios")

# Verifica se a requisição foi bem-sucedida (código 200)
if response.status_code == 200:
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
        response_sparql = requests.post(endpoint_url, data=parametros)

        # Verificação do status da resposta
        if response_sparql.status_code == 200:
            # Obtenção dos resultados
            resultados = response_sparql.json()

            # Transforma os resultados em uma lista de dicionários
            dados_tabela = []
            for resultado in resultados["results"]["bindings"]:
                linha = {chave: valor['value'] for chave, valor in resultado.items()}
                dados_tabela.append(linha)

            # Remover a parte específica da string dos resultados
            for linha in dados_tabela:
                for chave in linha:
                    if isinstance(linha[chave], str) and linha[chave].startswith("https://web.bdij.com.br/entity/"):
                        linha[chave] = linha[chave][len("https://web.bdij.com.br/entity/"):]

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

        else:
            print(f"Falha na requisição SPARQL. Código de status: {response_sparql.status_code}")

    else:
        print("Tag <pre> não encontrada na página.")
else:
    print(f"Falha na requisição HTTP. Código de status: {response.status_code}")
