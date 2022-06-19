from flask import Blueprint, request, render_template, make_response, jsonify
from regist_ingredient import Register
from .thread import MyThread
import pandas as pd

regist_router = Blueprint('regist_ingredient', __name__)
register = Register()

@regist_router.route('/regist', methods=['POST'])
def regist_ingredient():
    ingredient = request.form['ingredient']
    amount = request.form['amount']
    ingredient_pro = register.regist_ingredient(ingredient, amount)
    spice_df = pd.read_csv('./api/data/spices.csv')
    spice = spice_df['spice'].values
    if ingredient_pro[0] not in spice:
        t = MyThread(ingredient)
        t.start()
    # 食材が追加された食材を記録
    return render_template('index.html', message="登録しました")