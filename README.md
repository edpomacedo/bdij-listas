# bdij-listas

![doi:10.5281/zenodo.10339637](https://zenodo.org/badge/DOI/10.5281/zenodo.10339637.svg)

Criação de tabelas wikitext a partir de consultas SPARQL na Base de Dados de Institutos Jurídicos.

## Estrutura

- `/tables`: Diretório para armazenamento das consultas renderizadas em tabela wikitext.

## Pré-requisitos

Requer-se as bibliotecas `requests`, `beautifulsoup4` e `tabulate`.

```bash
pip install -r requirements.txt
```

## Instalação

```bash
git clone https://github.com/edpomacedo/bdij-listas.git
cd bdij-listas
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

1. Acesse uma página no espaço nominal `Project:` da Base de Dados de Institutos Jurídicos.
2. Verifique se existe uma página de discussão do referido projeto, contendo uma consulta SPARQL entre as tags `<pre>`.
3. Copie a URL da página de discussão do projeto que contém a consulta SPARQL e cole na linha 11 do arquivo `main.py`
4. Execute o comando `python main.py`.

Será gerado um `arquivo.txt` dentro da pasta `./tables`, contendo o resultado da consulta formatado em tabela wikitext.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para a sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adicione uma nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Copyright 2023 EDPO AUGUSTO FERREIRA MACEDO

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contato

[Base de Dados de Institutos Jurídicos](https://github.com/bdij)