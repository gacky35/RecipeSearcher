from flask import Blueprint, request, make_response, jsonify

regist_router = Blueprint('regist_ingredient', __name__)

@regist_router.route('/regist', methods=['GET', 'POST'])
def regist_ingredient():
    if request.method == 'GET':
        return 'get ingredient'
    # 食材が追加された食材を記録
    return 'ingredient'