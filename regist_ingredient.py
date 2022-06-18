import pandas as pd
from crawl_recipe import Crawler

class Register:
    def __init__(self):
        self.Crawler = Crawler()

    def regist_ingredient(self, ingredient, amount):
        ingredient = self.Crawler.get_pronunciation([ingredient])
        amount = self.Crawler.replace_to_gram(amount)
        ingredient_df = pd.read_csv('/api/data/ingredient.csv')
        if ingredient_df[ingredient]:
            ingredient_df[ingredient] += amount
        else:
            ingredient_df[ingredient] = amount
        ingredient_df.to_csv('/api/data/ingredient.csv', index=False)
        spice_df = pd.read_csv('/api/data/spice.csv')
        spice = spice_df['spice'].values
        if ingredient not in spice:
            self.Crawler.crawl_recipe(ingredient)