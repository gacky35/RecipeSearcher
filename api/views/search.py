from flask import Blueprint, request, make_response, jsonify
from crawl_recipe import Crawler

search_router = Blueprint('search_recipe', __name__)

@search_router.route('/search', methods=['POST'])
def search_recipe():
    # 食材が追加されたときに非同期でやりたさある
    if request.method == 'GET':
        return 'get search recipe'
    return 'search recipe'

@search_router.route("/search_menu", methods=["POST"])
def search_menu():
    if request.method == 'GET':
        return 'get search menu'
    return "search menu"