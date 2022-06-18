import pandas as pd
from crawl_recipe import Crawler
# wv = cr.crawl
class Proposer:
    def __init__(self):
        self.crawler = Crawler()

    def extract_recipe(self, knapsack, wv):
        tmp = wv.copy()
        wv = wv.drop(knapsack.columns.values, axis=1)
        wv['sum'] = wv.sum(axis=1)
        tmp.iloc[wv[wv['sum'] == 0].index.values]

    def solve_knapsack(self):
        knapsack = pd.read_csv('./api/data/ingredient.csv')
        wv = self.crawler.recipe_candidate()
        recipe = wv['link']
        wv = wv.drop('link', axis=1)
        wv = self.extract_recipe(knapsack, wv)
        print(wv)
        W = sum(knapsack.iloc[0].values)
        dp = [[0] * (W + 1) for _ in range(len(wv)+1)]
        amount = knapsack.iloc[0].values
        dp_ks = [[amount] * (W + 1) for _ in range(len(wv)+1)]
        choice = [[""] * (W + 1) for _ in range(len(wv)+1)]
        for idx, row in wv.iterrows():
            for j in range(W+1):
                dp[idx+1][j] = dp[idx][j]
                choice[idx+1][j] = choice[idx][j] + '0'
                dp_ks[idx+1][j] = dp_ks[idx][j]
                # if j - sum(row.values) >= 0 and all(knapsack["amount"] >= row.values):
                if j - sum(row.values) >= 0 and all(dp_ks[idx+1][j] >= row.values):
                    if dp[idx+1][j] < dp[idx][j-sum(row.values)] + sum(row.values):
                        dp[idx+1][j] = dp[idx][j-sum(row.values)] + sum(row.values)
                        dp_ks[idx+1][j] = dp_ks[idx][j-sum(row.values)] - row.values
                        choice[idx+1][j] = choice[idx][j-sum(row.values)] + "1"
        print(choice[-1][-1])
# knapsack = pd.DataFrame({"ingredient": ["大根", "にんじん", "卵", "豚バラ肉", "キャベツ", "塩", "酢", "砂糖", "みりん", "しょうゆ", "黒こしょう", "ワカメ", "鶏ガラスープの素", "ゴマ油", "塩こしょう", "ごはん", "コンソメ顆粒", "酒"], "amount": [900, 150, 2, 300, 150, 100, 100, 100, 100, 100, 20, 5, 300, 100, 100, 500, 200, 100]})
# data_list = [
#     [0, 0, 1, 0, 50, 0.45, 0, 0, 0, 0, 0.45, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 5, 0, 2, 10, 5, 0.45, 0, 0, 0],
#     [0, 0, 2, 150, 0, 0.45, 0, 5, 15, 15, 0, 0, 0, 0, 0, 200, 0, 0],
#     [50, 50, 0, 0, 0, 0.45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0],
#     [400, 0, 0, 200, 0, 0, 0, 30, 30, 30, 0, 0, 0, 15, 0, 0, 0, 30]
# ]
# wv = pd.DataFrame(data_list, columns=["大根", "にんじん", "卵", "豚バラ肉", "キャベツ", "塩", "酢", "砂糖", "みりん", "しょうゆ", "黒こしょう", "ワカメ", "鶏ガラスープの素", "ゴマ油", "塩こしょう", "ごはん", "コンソメ顆粒", "酒"])
# recipe = ["巣ごもり卵", "ワカメスープ", "他人丼", "ニンジンスープ", "豚バラ大根"]

# df = pd.DataFrame()
# wv = extract_recipe(knapsack, wv)
# W = sum(knapsack.iloc[0].values)
# dp = [[0] * (W + 1) for _ in range(len(wv)+1)]
# amount = knapsack.iloc[0].values
# dp_ks = [[amount] * (W + 1) for _ in range(len(wv)+1)]
# choice = [[""] * (W + 1) for _ in range(len(wv)+1)]
# for idx, row in wv.iterrows():
#     for j in range(W+1):
#         dp[idx+1][j] = dp[idx][j]
#         choice[idx+1][j] = choice[idx][j] + '0'
#         dp_ks[idx+1][j] = dp_ks[idx][j]
#         # if j - sum(row.values) >= 0 and all(knapsack["amount"] >= row.values):
#         if j - sum(row.values) >= 0 and all(dp_ks[idx+1][j] >= row.values):
#             if dp[idx+1][j] < dp[idx][j-sum(row.values)] + sum(row.values):
#                 dp[idx+1][j] = dp[idx][j-sum(row.values)] + sum(row.values)
#                 dp_ks[idx+1][j] = dp_ks[idx][j-sum(row.values)] - row.values
#                 choice[idx+1][j] = choice[idx][j-sum(row.values)] + "1"
# print(choice[-1][-1])
# print(dp[-1][-1])
# sum(knapsack.iloc[0].values)
# def calc_knapsack(i, w, wv, knapsack, choice):
#     if (i >= len(wv)):
#         return 0, ''
#     elif w - sum(wv.iloc[i].values) < 0 or any(knapsack < wv.iloc[i].values):
#         return calc_knapsack(i+1, w, wv, knapsack, choice + '0')
#     else:
#         p1, c1 = calc_knapsack(i+1, w, wv, knapsack, choice + '0')
#         p2, c2 = calc_knapsack(i+1, w - sum(wv.iloc[i].values), wv, knapsack - wv.iloc[i].values, choice + '1')
#         p2 += sum(wv.iloc[i].values)
#         if p1 > p2:
#             return p1, c1 + str(i)
#         else:
#             return p2, c2 + str(i)
# p = calc_knapsack(0, sum(knapsack["amount"]), wv, knapsack["amount"], '')
# print(p)
# knapsack["amount"] - wv.iloc[0].values
# df_sample = wv.iloc[1].values + wv.iloc[3].values + wv.iloc[4].values
# print(sum(df_sample))
# for i in range(1, len(wv)):
#     df_sample += wv.iloc[i].values
# print(sum(df_sample.iloc[0]))
# print(knapsack["amount"] - df_sample.iloc[0].values)
# def extract_recipe(knapsack, wv):
#     tmp = wv.copy()
#     wv = wv.drop(knapsack.columns.values, axis=1)
#     wv['sum'] = wv.sum(axis=1)
#     tmp.iloc[wv[wv['sum'] == 0].index.values]