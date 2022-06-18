import pandas as pd
from flask import Blueprint, request, make_response, jsonify
from crawl_recipe import Crawler
from propose_menu import Proposer

search_router = Blueprint('search_recipe', __name__)
Crawler = Crawler()
Proposer = Proposer()

@search_router.route('/search', methods=['POST'])
def search_recipe():
    spice_df = pd.read_csv('/api/data/spice.csv')
    spice = spice_df['spice'].values
    if request.form['ingredient'] not in spice:
        Crawler.crawl_recipe(request.form['ingredient'])
    # 食材が追加されたときに非同期でやりたさある
    return 'search recipe'

@search_router.route("/search_menu", methods=["POST"])
def search_menu():
    menu_df = Proposer.solve_knapsack()
    return "search menu"