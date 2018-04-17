import plotly
import plotly.graph_objs as go
from model import *


def get_unique_chart_name(chart_type='bar', db_name=DB_NAME, lang='en', x_name='region', y_name='unit_price'):
    params = [chart_type, lang, y_name, x_name, db_name]
    fname = '-'.join(params) + '.html'
    return fname


def plot_bar_chart(db_name=DB_NAME, lang='en', x_name='region', y_name='unit_price'):
    """
    plot bar charts in plotly
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :param x_name: options: region, num_bd, size_level, price_level
    :param y_name: options: total_price, total_area, unit_price
    :return: a bar chart
    """

    if lang == 'en':
        title = 'Shanghai Second-hand Housing'
        if x_name == 'region':
            x_title = 'Region Name'
        elif x_name == 'num_bd':
            x_title = 'Number of Bedrooms'
        elif x_name == 'size_level':
            x_title = 'Size Level'
        elif x_name == 'price_level':
            x_title = 'Price Level'
        else:
            return None

        if y_name == 'total_price':
            y_title = 'Total Price (K USD)'
        elif y_name == 'total_area':
            y_title = 'Total Area (SQ FT)'
        elif y_name == 'unit_price':
            y_title = 'Unit Price (USD/SQ FT)'
        else:
            return None

    elif lang == 'zh':
        title = '上海二手房价'
        if x_name == 'region':
            x_title = '区域'
        elif x_name == 'num_bd':
            x_title = '户型'
        elif x_name == 'size_level':
            x_title = '面积'
        elif x_name == 'price_level':
            x_title = '总价'
        else:
            return None

        if y_name == 'total_price':
            y_title = '总价（万元）'
        elif y_name == 'total_area':
            y_title = '面积（平米）'
        elif y_name == 'unit_price':
            y_title = '单价（元/平米）'
        else:
            return None

    else:
        return None

    layout = dict(
        title=title,
        xaxis=dict(
            title=x_title,
        ),
        yaxis=dict(
            title=y_title
        )
    )

    x_lst = []
    y_lst = []
    fname = get_unique_chart_name(chart_type='bar', db_name=db_name, lang=lang, x_name=x_name, y_name=y_name)
    fdest = 'charts/bar/' + fname

    """the first bar is always all shanghai average"""
    all_sh_avg = get_avgs(db_name=db_name, lang=lang, data=y_name, group=None)[0]
    y_lst.append(all_sh_avg)
    if lang == 'en':
        x_lst.append('ALL')
    elif lang == 'zh':
        x_lst.append('全上海')
    else:
        return None

    """use id_lst as index for x_lst and y_lst"""
    if y_name in ['total_price', 'total_area', 'unit_price']:
        data_dict = get_avgs(db_name=db_name, lang=lang, data=y_name, group=x_name)
    else:
        return None

    if x_name == 'region':
        region_dict = get_new_region_dict(db_name=db_name, lang=lang)
        id_lst = list(region_dict.keys())
        for i in id_lst:
            x_lst.append(region_dict[i])
            y_lst.append(data_dict[i])
    elif x_name == 'num_bd':
        id_lst = get_style_lst(db_name=db_name)
        if lang == 'zh':
            for i in id_lst:
                x_lst.append(str(i)+'室')
                y_lst.append(data_dict[i])
        elif lang == 'en':
            for i in id_lst:
                x_lst.append(str(i)+'Rms')
                y_lst.append(data_dict[i])
        else:
            return None
    elif x_name == 'size_level':
        size_dict = get_size_level_dict(db_name=db_name, lang=lang)
        id_lst = list(size_dict.keys())
        for i in id_lst:
            x_lst.append(str(size_dict[i]))
            y_lst.append(data_dict[i])
    elif x_name == 'price_level':
        price_dict = get_price_level_dict(db_name=db_name, lang=lang)
        id_lst = list(price_dict.keys())
        for i in id_lst:
            x_lst.append(str(price_dict[i]))
            y_lst.append(data_dict[i])
    else:
        return None

    data = [go.Bar(
        x=x_lst,
        y=y_lst
    )]
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename=fdest)


def plot_scatter_chart(db_name=DB_NAME, lang='en', x_name='density', y_name='unit_price'):
    """
    plot scatter chart (each point represents one district in Shanghai)
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :param x_name: options: density/gdp(per capita)
    :param y_name: unit_price
    :return: a scatter plot
    """

    if lang == 'en':
        title = 'Shanghai Second-hand Housing'
        if x_name == 'density':
            x_title = 'Density (K/Sq Mi)'
        elif x_name == 'gdp':
            x_title = 'GDP Per Capita (K USD)'
        else:
            return None

        if y_name == 'unit_price':
            y_title = 'Unit Price (USD/SQ FT)'
        else:
            return None

    elif lang == 'zh':
        title = '上海二手房价'
        if x_name == 'density':
            x_title = '人口密度（万人/平方公里）'
        elif x_name == 'gdp':
            x_title = '人均GDP（万元）'
        else:
            return None

        if y_name == 'unit_price':
            y_title = '单价（元/平米）'
        else:
            return None

    else:
        return None

    layout = dict(
        title=title,
        xaxis=dict(
            title=x_title,
        ),
        yaxis=dict(
            title=y_title
        )
    )

    fname = get_unique_chart_name(chart_type='scatter', db_name=db_name, lang=lang, x_name=x_name, y_name=y_name)
    fdest = 'charts/scatter/' + fname
    x_lst = []
    y_lst = []
    name_lst = []

    get_new_region_data()
    id_lst = range(1, 17)
    region_dict = get_new_region_dict(db_name=db_name, lang=lang)
    x_data_dict = get_new_region_data(db_name=db_name, data=x_name)
    y_data_dict = get_avgs(db_name=db_name, lang=lang, data=y_name, group='region')

    for i in id_lst:
        name_lst.append(region_dict[i])
        x_lst.append(x_data_dict[i])
        y_lst.append(y_data_dict[i])
    print(name_lst)

    data = [go.Scatter(
        x=x_lst,
        y=y_lst,
        text=name_lst,
        mode='markers'
    )]

    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename=fdest)


def plot_bars():
    for lang in ['en', 'zh']:
        for x_name in ['region', 'num_bd', 'price_level', 'size_level']:
            for y_name in ['total_price', 'total_area', 'unit_price']:
                plot_bar_chart(db_name=DB_NAME, lang=lang, x_name=x_name, y_name=y_name)


def plot_scatters():
    for lang in ['en', 'zh']:
        for x_name in ['density', 'gdp']:
            for y_name in ['unit_price']:
                plot_scatter_chart(db_name=DB_NAME, lang=lang, x_name=x_name, y_name=y_name)


if __name__ == '__main__':
    # print(get_unique_chart_name())
    # plot_bars()
    plot_scatters()
    pass

