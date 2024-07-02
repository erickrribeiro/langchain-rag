import requests
from bs4 import BeautifulSoup

website = 'https://dieboldnixdorf.com.br/automacao-bancaria/servicos/'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
box = soup.find('body')

links = [link['href'] for link in box.find_all('a', href=True)]
print(links)
with open('output.txt', 'a', encoding='utf-8') as file:

    for link in links[1:]:
        if link != 'https://dieboldnixdorf.com.br/suporte/':
            result = requests.get(link)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            box = soup.find('body')
            file.write(box.text + '\n')
            print(link)
            # h1 = [link['href'] for link in box.find_all('a', href=True)]


