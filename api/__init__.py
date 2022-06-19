from flask import Flask, make_response, jsonify
from .views.search import search_router
from .views.regist import regist_router

def create_app():
    app = Flask(__name__, static_folder='./templates/img')
    app.register_blueprint(search_router, url_prefix='/api')
    app.register_blueprint(regist_router, url_prefix='/api')
    return app

app = create_app()