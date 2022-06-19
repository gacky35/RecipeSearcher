import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import MeCab
import jaconv
import glob
import copy

class Crawler:
    def __init__(self):
        self.base_url = 'https://www.kurashiru.com'
        self.crawl_url = "https://kurashiru.com/search?query="
        self.replace_data = {"大さじ": 15, "小さじ": 5, "少々": 0.4, "ひとつまみ": 0.7, "ふたつまみ": 1.4, "本": 300, "適量": 0.3, "お好みで":0.3}
        self.morpho = MeCab.Tagger()

    def agg_dup_col(self, df_):
        df = df_.copy()
        dup_col = set(df.columns[df.columns.duplicated()])
        for col in dup_col:
            value = [[v for v in values if v == v and v is not None] for values in df[col].values.tolist()]
            value = [sum(v) if v != [] else None for v in value]
            df = df.drop(col, axis=1)
            df[col] = value
        return df

    def replace_to_gram(self, x):
        x = jaconv.z2h(x, kana=False, digit=True)
        m = re.match(r"([^0-9/.]+)?([0-9/.]+)?([^0-9/.]+)?", x)
        if m.groups()[1] is None:
            return self.replace_data[m.groups()[0]]
        elif m.groups()[0] in self.replace_data:
            return eval(m.groups()[1]) * self.replace_data[m.groups()[0]]
        elif m.groups()[2] in self.replace_data:
            return eval(m.groups()[1]) * self.replace_data[m.groups()[2]]
        else:
            return eval(m.groups()[1])

    def get_pronunciation(self, ingredients):
        pronunciations = []
        for ingredient in ingredients:
            morpho_result = self.morpho.parse(ingredient).splitlines()[:-1]
            pronunciation = ''
            for v in morpho_result:
                if '\t' not in v:
                    continue
                surface = v.split('\t')[0]
                p = v.split('\t')[-1].split(',')[-2]
                if p == '*':
                    p = surface
                pronunciation += p
            pronunciations.append(pronunciation)
        pronunciations = [jaconv.kata2hira(pro) for pro in pronunciations]
        return pronunciations

    def crawl_recipe(self, ingredient):
        csv = glob.glob(ingredient)
        if len(csv) > 0:
            recipe_df = pd.read_csv(csv[0])
            return recipe_df
        url = self.crawl_url + ingredient
        site = requests.get(url)
        html = BeautifulSoup(site.text, 'html.parser')
        page_url_list = [self.base_url + a['href'] for a in html.find_all('a', class_="DlyLink pagenate-button pagenate-button")]
        page_url_list = page_url_list[:2] if len(page_url_list) > 2 else page_url_list
        detail_url_list = [self.base_url + a['href'] for a in html.find_all('a', class_="DlyLink title")]
        recipes = pd.DataFrame()
        # title = []
        link = copy.copy(detail_url_list)
        for detail_url in detail_url_list:
            try:
                recipe = BeautifulSoup(requests.get(detail_url).text, 'html.parser')
                span = recipe.find_all('span', class_="servings")
                serving = re.match(r'(\d+)', span[0].get_text().strip('(')).groups()[0]
                # title.append(recipe.find_all('h1', class_="title")[0].get_text().split('　')[0])
                ingredients = [[re.sub('\([^\)]+\)', '', li.a.get_text().strip()), self.replace_to_gram(li.span.get_text()) / (eval(serving) if eval(serving) <= 30 else 1)] for li in recipe.find_all('li', class_='ingredient-list-item') if li.a is not None]
                ingredients_df = pd.DataFrame([[x[1] for x in ingredients]], columns=[x[0] for x in ingredients])
                ingredients_df = self.agg_dup_col(ingredients_df)
                recipes = pd.concat([recipes, ingredients_df], ignore_index=True)
            except:
                link.remove(detail_url)
            time.sleep(1)
        recipes = recipes.fillna(0)
        normalize_ingreadients = self.get_pronunciation(recipes.columns.values)
        recipes = recipes.set_axis(normalize_ingreadients, axis='columns')
        recipes = self.agg_dup_col(recipes)
        # return self.crawl_recipe_sub(page_url_list, recipes, title, link, ingredient)
        return self.crawl_recipe_sub(page_url_list, recipes, link, ingredient)

    # def crawl_recipe_sub(self, page_url_list, recipes, title, link, ingredient):
    def crawl_recipe_sub(self, page_url_list, recipes, link, ingredient):
        for page_url in page_url_list:
            html = BeautifulSoup(requests.get(page_url).text, 'html.parser')
            detail_url_list = [self.base_url + a['href'] for a in html.find_all('a', class_="DlyLink title")]
            link.extend(detail_url_list)
            for detail_url in detail_url_list:
                try:
                    recipe = BeautifulSoup(requests.get(detail_url).text, 'html.parser')
                    span = recipe.find_all('span', class_="servings")
                    serving = re.match(r'(\d+)', span[0].get_text().strip('(')).groups()[0]
                    # title.append(recipe.find_all('h1', class_="title")[0].get_text().split('　')[0])
                    ingredients = [[re.sub('\([^\)]+\)', '', li.a.get_text().strip()), self.replace_to_gram(li.span.get_text()) / (eval(serving) if eval(serving) <= 30 else 1)] for li in recipe.find_all('li', class_='ingredient-list-item') if li.a is not None]
                    ingredients_df = pd.DataFrame([[x[1] for x in ingredients]], columns=[x[0] for x in ingredients])
                    ingredients_df = self.agg_dup_col(ingredients_df)
                    recipes = pd.concat([recipes, ingredients_df], ignore_index=True)
                except:
                    link.remove(detail_url)
                time.sleep(1)
        recipes = recipes.fillna(0)
        normalize_ingreadients = self.get_pronunciation(recipes.columns.values)
        recipes = recipes.set_axis(normalize_ingreadients, axis='columns')
        # recipes = recipes.set_axis(title, axis='index')
        recipes = self.agg_dup_col(recipes)
        recipes['link'] = link
        ingredient = self.get_pronunciation([ingredient])[0]
        recipes.to_csv('./api/data/' + ingredient + '.csv', index=False)
        return recipes

    def recipe_candidate(self):
        ingredient_df = pd.read_csv('./api/data/ingredient.csv')
        ingredients = ingredient_df.columns.values
        recipe_candidates = pd.DataFrame()
        for ingredient in ingredients:
            try:
                recipe_candidate = pd.read_csv('./api/data/'+ingredient+'.csv')
                recipe_candidates = pd.concat([recipe_candidates, recipe_candidate], ignore_index=True)
            except:
                pass
        recipe_candidates = self.agg_dup_col(recipe_candidates)
        recipe_candidates = recipe_candidates.fillna(0)
        return recipe_candidates

    def get_title(self, links):
        titles = []
        for url in links:
            site = requests.get(url)
            html = BeautifulSoup(site.text, 'html.parser')
            title = html.title.text
            titles.append(title)
        return titles
