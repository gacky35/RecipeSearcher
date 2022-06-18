#%%
import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
from urllib.parse import urljoin
import re
#%%
base_url = 'https://www.kurashiru.com'
crawl_url = "https://kurashiru.com/search?query="
#%%
site = requests.get(crawl_url)
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
ingredients = [[re.sub('\([^\)]+\)', '', li.a.get_text().strip()), li.span.get_text()] for li in recipe.find_all('li', class_='ingredient-list-item')]
print(ingredients)
#%%
def agg_dup_col(df_):
    df = df_.copy()
    dup_col = set(df.columns[df.columns.duplicated()])
    for col in dup_col:
        value = [[v for v in values if v == v and v is not None] for values in df[col].values.tolist()]
        value = [sum(v) if v != [] else None for v in value]
        df = df.drop(col, axis=1)
        df[col] = value
    return df
#%%
replace_data = {"大さじ": 15, "小さじ": 5, "少々": 0.4, "ひとつまみ": 0.7, "ふたつまみ": 1.4, "本": 300, "適量": 0.3}
#%%
def replace_to_gram(x):
    m = re.match(r"([^0-9/.]+)?([0-9/.]+)?([^0-9/.]+)?", x)
    if m.groups()[1] is None:
        return replace_data[m.groups()[0]]
    elif m.groups()[0] in replace_data:
        return eval(m.groups()[1]) * replace_data[m.groups()[0]]
    elif m.groups()[2] in replace_data:
        return eval(m.groups()[1]) * replace_data[m.groups()[2]]
    else:
        return eval(m.groups()[1])
#%%
def crawl_recipe(ingredient):
    url = crawl_url + ingredient
    site = requests.get(url)
    html = BeautifulSoup(site.text, 'html.parser')
    page_url_list = [base_url + a['href'] for a in html.find_all('a', class_="DlyLink pagenate-button pagenate-button")]
    page_url_list = page_url_list[:2] if len(page_url_list) > 2 else page_url_list
    detail_url_list = [base_url + a['href'] for a in html.find_all('a', class_="DlyLink title")]
    recipes = pd.DataFrame()
    for detail_url in detail_url_list:
        recipe = BeautifulSoup(requests.get(detail_url).text, 'html.parser')
        ingredients = [[re.sub('\([^\)]+\)', '', li.a.get_text().strip()), replace_to_gram(li.span.get_text())] for li in recipe.find_all('li', class_='ingredient-list-item') if li.a is not None]
        ingredients_df = pd.DataFrame([[x[1] for x in ingredients]], columns=[x[0] for x in ingredients])
        ingredients_df = agg_dup_col(ingredients_df)
        recipes = pd.concat([recipes, ingredients_df], ignore_index=True)
        time.sleep(1)
    return crawl_recipe_sub(page_url_list, recipes.fillna(0))
#%%
def crawl_recipe_sub(page_url_list, recipes):
    for page_url in page_url_list:
        html = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        detail_url_list = [base_url + a['href'] for a in html.find_all('a', class_="DlyLink title")]
        for detail_url in detail_url_list:
            recipe = BeautifulSoup(requests.get(detail_url).text, 'html.parser')
            ingredients = [[re.sub('\([^\)]+\)', '', li.a.get_text().strip()), replace_to_gram(li.span.get_text())] for li in recipe.find_all('li', class_='ingredient-list-item') if li.a is not None]
            ingredients_df = pd.DataFrame([[x[1] for x in ingredients]], columns=[x[0] for x in ingredients])
            ingredients_df = agg_dup_col(ingredients_df)
            recipes = pd.concat([recipes, ingredients_df], ignore_index=True)
            time.sleep(1)
    return recipes.fillna(0)
# %%
start = time.time()
recipe_df = crawl_recipe("きゅうり")
display(recipe_df)
print(time.time() - start)
# %%
