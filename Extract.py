from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import math
import re
import time
import pandas as pd

options = Options()
options.add_argument('--headless')  # roda invisível
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=options
)


url_base = 'https://www.kabum.com.br/celular-smartphone'
driver.get(url_base)

# Espera o contador aparecer
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'listingCount'))
)

soup = BeautifulSoup(driver.page_source, 'html.parser')
div_listing = soup.find('div', id='listingCount')
total_produtos = int(div_listing.find('b').get_text(strip=True))
ultima_pagina = math.ceil(total_produtos / 20)
dic_produtos = {'nome': [], 'preco': [], 'parcela': []}

print(f'Total de produtos: {total_produtos}')
print(f'Última página: {ultima_pagina}')

# Aqui limitamos para teste em só 2 páginas
for i in range(1, ultima_pagina+1):
    print(f'\n📄 Página {i}')
    url_pag = f'https://www.kabum.com.br/celular-smartphone?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    driver.get(url_pag)

    # Espera os produtos aparecerem
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    produtos = soup.find_all('article', class_=re.compile('productCard'))

    for produto in produtos:
        nome_tag = produto.find('span', class_=re.compile('nameCard'))
        preco_tag = produto.find('span', class_=re.compile('priceCard'))
        parcela_tag = produto.find('b', class_=re.compile(
            'desktop:leading-4'))

        if nome_tag and preco_tag:
            nome = nome_tag.get_text(strip=True)
            preco = preco_tag.get_text(strip=True)
            parcela = parcela_tag.get_text(strip=True)
            print(nome, preco, parcela)

            dic_produtos['nome'].append(nome)
            dic_produtos['preco'].append(preco)
            dic_produtos['parcela'].append(parcela)

df = pd.DataFrame(dic_produtos)
df.to_csv('produtos.csv', sep=';')

driver.quit()
