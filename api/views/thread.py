import threading
from datetime import datetime
from time import sleep
from flask import Blueprint, request, make_response, jsonify
from crawl_recipe import Crawler

class MyThread(threading.Thread):
    def __init__(self, ingredient):
        super(MyThread, self).__init__()
        self.stop_event = threading.Event()
        self.ingredient = ingredient

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            crawler = Crawler()
            crawler.crawl_recipe(self.ingredient) #検索に飛ばす
        finally:
            print('done')

thread_router = Blueprint('control_thread', __name__)

@thread_router.route('/run/<ingredient>')
def run(ingredient):
    t = MyThread(ingredient)
    t.start()
    return make_response(f'{id}の処理を受け付けた'), 202
