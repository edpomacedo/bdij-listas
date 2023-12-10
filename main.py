import requests
from bs4 import BeautifulSoup

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
            # Impressão dos resultados
            resultados = response_sparql.json()
            for resultado in resultados["results"]["bindings"]:
                for chave, valor in resultado.items():
                    print(f"{chave}: {valor['value']}")
                print("------")
        else:
            print(f"Falha na requisição SPARQL. Código de status: {response_sparql.status_code}")

    else:
        print("Tag <pre> não encontrada na página.")
else:
    print(f"Falha na requisição HTTP. Código de status: {response.status_code}")
