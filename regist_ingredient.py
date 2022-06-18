import pandas as pd
import glob
from crawl_recipe import Crawler

class Register:
    def __init__(self):
        self.Crawler = Crawler()

    def regist_ingredient(self, ingredient, amount):
        ingredient = self.Crawler.get_pronunciation([ingredient])
        amount = self.Crawler.replace_to_gram(amount)
        csv = glob.glob('./api/data/ingredient.csv')
        if len(csv) > 0:
            ingredient_df = pd.read_csv('./api/data/ingredient.csv')
        else:
            ingredient_df = pd.DataFrame()
        if len(ingredient_df) == 0 or ingredient[0] not in ingredient_df.columns:
            ingredient_df[ingredient[0]] = [amount]
        else:
            ingredient_df[ingredient[0]] += amount
        ingredient_df.to_csv('./api/data/ingredient.csv', index=False)
        return ingredient