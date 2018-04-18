from flask import Flask, render_template, request
from model import *
import json
from charts_plotly import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/zh/')
def index_zh():
    return render_template('index_zh.html')


@app.route('/search/')
def search():
    region_dict = get_old_region_dict(DB_NAME, lang='en')
    region_dict[0] = 'ALL'
    return render_template('search.html', region_dict=region_dict)


@app.route('/search/zh/')
def search_zh():
    region_dict = get_old_region_dict(DB_NAME, lang='zh')
    region_dict[0] = 'ALL'
    return render_template('search_zh.html', region_dict=region_dict)


@app.route('/chart/', methods=['GET', 'POST'])
def chart():
    div = '<div></div>'
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        chart_type = request.form['type']
        if chart_type == 'bar':
            div = plot_bar_chart(db_name=DB_NAME, lang='en', x_name=x, y_name=y)
            div = div if div is not None else '<div></div>'
        elif chart_type == 'scatter':
            div = plot_scatter_chart(db_name=DB_NAME, lang='en', x_name=x, y_name=y)
            div = div if div is not None else '<div></div>'
    return render_template('chart.html', div=div)


@app.route('/chart/zh/', methods=['GET', 'POST'])
def chart_zh():
    div = '<div></div>'
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        chart_type = request.form['type']
        if chart_type == 'bar':
            div = plot_bar_chart(db_name=DB_NAME, lang='zh', x_name=x, y_name=y)
            div = div if div is not None else '<div></div>'
        elif chart_type == 'scatter':
            div = plot_scatter_chart(db_name=DB_NAME, lang='zh', x_name=x, y_name=y)
            div = div if div is not None else '<div></div>'
    return render_template('chart_zh.html', div=div)


@app.route('/search/data/', methods=["GET"])
def search_data():
    region_lst = request.args.get('region_lst')
    area_result = []
    if (region_lst != '') and (region_lst is not None):
        for region_id in region_lst.split(','):
            area_result += table_get_housing_posts(lang='en', group='region', group_id=int(region_id))
    return json.dumps(area_result)


@app.route('/search/data/zh/', methods=["GET"])
def search_data_zh():
    region_lst = request.args.get('region_lst')
    area_result = []
    print(area_result)
    if (region_lst != '') and (region_lst is not None):
        for region_id in region_lst.split(','):
            area_result += table_get_housing_posts(lang='zh', group='region', group_id=int(region_id))
    return json.dumps(area_result)


if __name__ == '__main__':
    app.run(debug=True)
