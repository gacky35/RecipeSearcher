#%%
import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
from urllib.parse import urljoin
#%%
base_url = 'https://www.kurashiru.com'
url = "https://kurashiru.com/search?query=酢のもの"
site = requests.get(url)
site.raise_for_status()
html = BeautifulSoup(site.text, 'html.parser')
#%%
detail_url_list = [base_url + a['href'] for a in html.find_all('a', class_="DlyLink title")]
print(detail_url_list)
#%%
page_url_list = [base_url + a['href'] for a in html.find_all('a', class_="DlyLink pagenate-button pagenate-button")]
print(page_url_list)
# %%
recipe_page = requests.get(detail_url_list[0])
recipe = BeautifulSoup(recipe_page.text, 'html.parser')
#%%
ingredients = [{'ingredient':li.a.get_text().strip(),'amount':li.span.get_text()} for li in recipe.find_all('li', class_='ingredient-list-item')]
print(ingredients)
