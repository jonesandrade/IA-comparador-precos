import requests
from bs4 import BeautifulSoup

def buscar_precos(produto):
    url = f"https://lista.mercadolivre.com.br/{produto}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    resultados = []
    # Pega os primeiros 5 produtos da busca
    for item in soup.find_all('li', class_='ui-search-layout__item', limit=5):
        nome = item.find('h2').text if item.find('h2') else "N/A"
        preco = item.find('span', class_='andes-money-amount__fraction').text if item.find('span', class_='andes-money-amount__fraction') else "0"
        link = item.find('a', class_='ui-search-link')['href'] if item.find('a', class_='ui-search-link') else ""
        
        resultados.append({"nome": nome, "preco": preco, "link": link})
    
    return resultados