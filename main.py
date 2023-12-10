import requests
from bs4 import BeautifulSoup

url = "https://web.bdij.com.br/wiki/Project_talk:Minist%C3%A9rios"

# Realiza a requisição HTTP para obter o conteúdo da página
response = requests.get(url)

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

        # Imprime a consulta SPARQL recuperada
        print(consulta_sparql)
    else:
        print("Tag <pre> não encontrada na página.")
else:
    print(f"Falha na requisição HTTP. Código de status: {response.status_code}")
