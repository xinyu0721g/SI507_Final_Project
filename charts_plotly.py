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
    :return:
    """

    x_lst = []
    y_lst = []
    fname = get_unique_chart_name(chart_type='bar', db_name=db_name, lang=lang, x_name=x_name, y_name=y_name)
    fdest = 'charts/' + fname

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
    id_lst = list(data_dict.keys())
    for i in id_lst:
        y_lst.append(data_dict[i])

    if x_name == 'region':
        region_dict = get_new_region_dict(db_name=db_name, lang=lang)
        for i in id_lst:
            x_lst.append(region_dict[i])
    elif x_name == 'num_bd':
        if lang == 'zh':
            for i in id_lst:
                x_lst.append(str(i)+'室')
        elif lang == 'en':
            for i in id_lst:
                x_lst.append(str(i)+'Rms')
        else:
            return None
    elif x_name == 'size_level':
        size_dict = get_size_level_dict(db_name=db_name, lang=lang)
        for i in id_lst:
            x_lst.append(str(size_dict[i]))
    elif x_name == 'price_level':
        price_dict = get_price_level_dict(db_name=db_name, lang=lang)
        for i in id_lst:
            x_lst.append(str(price_dict[i]))
    else:
        return None

    data = [go.Bar(
        x=x_lst,
        y=y_lst
    )]
    plotly.offline.plot(data, filename=fdest)


def plot_scatter_chart():
    pass


if __name__ == '__main__':
    plot_bar_chart(db_name=DB_NAME, lang='en', x_name='region', y_name='unit_price')
    # print(get_unique_chart_name())
    pass
