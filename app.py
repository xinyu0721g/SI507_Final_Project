from flask import Flask, render_template, request
from model import *
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    area_lst = get_old_region_dict(DB_NAME, lang='en')
    area_lst.insert(0, 'ALL')
    return render_template('search.html', area_lst=area_lst)


@app.route('/search/data/', methods=["GET"])
def search_data():
    area_lst = request.args.get('area_lst')
    print(area_lst)
    area_result = []
    for area in area_lst.split(','):
        area_result += table_get_housing_posts(lang='en', group='region', group_name=area)
    return json.dumps(area_result)


@app.route('/cn')
def cn():
    pass


@app.route('/en')
def en():
    pass


if __name__ == '__main__':
    app.run(debug=True)
