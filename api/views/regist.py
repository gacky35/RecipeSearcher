from flask import Blueprint, request, make_response, jsonify
from regist_ingredient import Register

regist_router = Blueprint('regist_ingredient', __name__)

@regist_router.route('/regist', methods=['POST'])
def regist_ingredient():
    ingredient = request.form['ingredient']
    amount = request.form['amount']
    print(ingredient, amount)
    # 食材が追加された食材を記録
    return 'ingredient'