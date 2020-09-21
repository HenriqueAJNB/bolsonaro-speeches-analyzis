import requests
from bs4 import BeautifulSoup
import os

# Loop throught the pages at url 
artigos = range(0, 271, 30)

# Create empty lists
titulos = []
urls = []
local_e_data = []

# Collect articles url's and title
for artigo in artigos:
    url = f"https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos?b_start:int={artigo}"

    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")
    
    a_tags = soup.find_all("a", attrs={"class":"summary url"})

    for a in a_tags:
        titulos.append(a.text)
        urls.append(a["href"])

# For each url and title collected, save the content in a text file.
for numeracao, url in enumerate(urls, 1):
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")

    b_tags = soup.find_all("b")

    for b in b_tags:
        local_e_data.append(b.text)

    p_tags = soup.find_all("p")
    print("Iniciar gravação dos arquivos!")
    for p in p_tags:
        nome_arquivo = f"arquivos/discurso_{numeracao}.txt"
        if os.path.exists(nome_arquivo):
            mode = 'a'
        else:
            mode = 'w'
        with open(nome_arquivo, mode) as arquivo:
            arquivo.write(p.text+"\n")