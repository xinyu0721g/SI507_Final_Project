import sqlite3

DB_NAME = 'Fang_db.sqlite'
DB_TEST = 'Fang_db_test.sqlite'


def get_old_region_dict(db_name=DB_NAME, lang='en'):
    """
    (for table use) get region name list with traditional region division
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :return: a dictionary where key is region id (old) and value is region name (old)
    """

    region_dict = {}
    db_dest = 'database/' + db_name
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        select_col = 'NameZh'
    elif lang == 'en':
        select_col = 'NameEn'
    else:
        return None

    statement = '''
        SELECT Id, {}
        FROM RegionsOld
    ;'''.format(select_col)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (region_id, region_name) in result_lst:
        region_dict[region_id] = region_name

    conn.close()
    return region_dict


def get_new_region_dict(db_name=DB_NAME, lang='en'):
    """
    (for chart use) get region name list with latest region division (after year 2015)
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :return: a dictionary where key is region id (new) and value is region name (new)
    """

    region_dict = {}
    db_dest = 'database/' + db_name
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        select_col = 'NewNameZh'
    elif lang == 'en':
        select_col = 'NewNameEn'
    else:
        return None

    statement = '''
        SELECT DISTINCT NewRegionId, {}
        FROM RegionsOld
    ;'''.format(select_col)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (region_id, region_name) in result_lst:
        region_dict[region_id] = region_name

    conn.close()
    return region_dict


def get_price_level_dict(db_name=DB_NAME, lang='en'):
    """
    get price level dictionary
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :return: a dictionary where key is price level id and value is price range of that level
    """

    price_dict = {}
    db_dest = 'database/' + db_name
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        select_col = 'PriceRange'
    elif lang == 'en':
        select_col = 'PriceRangeEn'
    else:
        return None

    statement = '''
        SELECT Id, {}
        FROM PriceLevels
    ;'''.format(select_col)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (price_level, price_range) in result_lst:
        price_dict[price_level] = price_range

    conn.close()
    return price_dict


def get_size_level_dict(db_name=DB_NAME, lang='en'):
    """
    get size level dictionary
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :return: a dictionary where key is size level id and value is size range of that level
    """

    size_dict = {}
    db_dest = 'database/' + db_name
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        select_col = 'SizeRange'
    elif lang == 'en':
        select_col = 'SizeRangeEn'
    else:
        return None

    statement = '''
        SELECT Id, {}
        FROM SizeLevels
    ;'''.format(select_col)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (size_level, size_range) in result_lst:
        size_dict[size_level] = size_range

    conn.close()
    return size_dict


def get_style_lst(db_name=DB_NAME):
    """
    get available style list
    :param db_name: database name, default DB_NAME
    :return: a list of available housing styles (number of bedrooms)
    """

    style_lst = []
    db_dest = 'database/' + db_name
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    statement = '''
        SELECT DISTINCT NumOfBd
        FROM Houses
        ORDER BY NumOfBd
    ;'''
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (num_of_bd,) in result_lst:
        style_lst.append(num_of_bd)

    conn.close()
    return style_lst


def get_avgs(db_name=DB_NAME, lang='en', data='unit_price', group=None):
    """
    get average total_price/total_area/unit_price for each group (if group=None, get data for all posts)
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :param data: returned data column, default unit_price (options: total_price/total_area/unit_price)
    :param group: group method, default None (options: None/region/num_bd/size_level/price_level)
    :return: a dictionary where key is group name and value is correlated average total_price/total_area/unit_price
    """

    return_dict = {}
    db_dest = 'database/' + db_name
    output_message = ''

    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        if data == 'total_price':
            data_column = 'AVG(TotalPriceCNY)'
            output_message += '：平均总价（万元）'
        elif data == 'total_area':
            data_column = 'AVG(TotalAreaSqM)'
            output_message += '：平均面积（平米）'
        elif data == 'unit_price':
            data_column = 'AVG(UnitPriceCNY)'
            output_message += '：平均单价（元/平米）'
        else:
            return None
    elif lang == 'en':
        if data == 'total_price':
            data_column = 'AVG(TotalPriceUSD)'
            output_message += ': Average Total Price (K USD)'
        elif data == 'total_area':
            data_column = 'AVG(TotalAreaSqFt)'
            output_message += ': Average Total Area (SQ FT)'
        elif data == 'unit_price':
            data_column = 'AVG(UnitPriceUSD)'
            output_message += ': Average Unit Price (USD/SQ FT)'
        else:
            return None
    else:
        return None

    if group is None:
        statement = '''
            SELECT {} FROM Houses      
        ;'''.format(data_column)
        value = cur.execute(statement).fetchone()[0]
        return_dict[0] = round(value, 2)
        if lang == 'zh':
            output_message = '全上海' + output_message
        else:
            output_message = 'All in Shanghai' + output_message

    elif group == 'region':
        if lang == 'zh':
            output_message = '区域' + output_message
        else:
            output_message = 'Region' + output_message
        statement = '''
            SELECT NewRegionId, {}
            FROM Houses
                JOIN RegionsOld
                    ON Houses.RegionId = RegionsOld.Id
            GROUP BY RegionsOld.NewRegionId
            ORDER BY {} DESC
        ;'''.format(data_column, data_column)
        result = cur.execute(statement)
        result_lst = result.fetchall()
        for (new_region_id, value) in result_lst:
            return_dict[new_region_id] = round(value, 2)

    elif group in ['num_bd', 'price_level', 'size_level']:
        if group == 'num_bd':
            group_by = 'NumOfBd'
            if lang == 'zh':
                output_message = '户型' + output_message
            else:
                output_message = 'Number of bedrooms' + output_message
        elif group == 'price_level':
            group_by = 'PriceLevel'
            if lang == 'zh':
                output_message = '总价' + output_message
            else:
                output_message = 'Price Level' + output_message
        else:
            group_by = 'SizeLevel'
            if lang == 'zh':
                output_message = '面积' + output_message
            else:
                output_message = 'Size Level' + output_message
        statement = '''
            SELECT {}, {}
            FROM Houses
            GROUP BY {}
            ORDER BY {} DESC
        ;'''.format(group_by, data_column, group_by, data_column)
        result = cur.execute(statement)
        result_lst = result.fetchall()
        for (group_name, value) in result_lst:
            return_dict[group_name] = round(value, 2)

    else:
        return None

    conn.close()

    # print('\n{' + output_message+'}')
    return return_dict


def get_new_region_data(db_name=DB_NAME, lang='en', data='density'):
    """
    get region information from RegionsNew table
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :param data: returned data column, default density (options: density/gdp(per capita))
    :return: a dictionary where key is region id and value is correlated density/gdp(per capita)
    """

    return_dict = {}
    db_dest = 'database/' + db_name
    output_message = ''

    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        output_message += '区域：'
        if data == 'density':
            data_column = 'Density10KSqKm'
            output_message += '人口密度（万人/平方公里）'
        elif data == 'gdp':
            data_column = 'GDPPerCapita10KCNY'
            output_message += '人均GDP（万元）'
        else:
            return None
    elif lang == 'en':
        output_message += 'Region: '
        if data == 'density':
            data_column = 'DensityKSqMi'
            output_message += 'Density (K/Sq Mi)'
        elif data == 'gdp':
            data_column = 'GDPPerCapitaKUSD'
            output_message += 'GDP Per Capita (K USD)'
        else:
            return None
    else:
        return None

    statement = '''
        SELECT Id, {} 
        FROM RegionsNew
        ORDER BY {} DESC
    ;'''.format(data_column, data_column)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (region_id, data_column) in result_lst:
        return_dict[region_id] = data_column

    conn.close()

    # print('\n{' + output_message+'}')
    return return_dict


def table_get_housing_posts(db_name=DB_NAME, lang='en', group=None, group_id=None):
    """
    get a list of house info dictionaries by group
    :param db_name: database name, default DB_NAME
    :param lang: language, default English (options: zh(Chinese)/en(English))
    :param group: group method, default None (options: None/region/num_bd/size_level/price_level)
    :param group_id: region_id/num_bd/size_level/price_level
    :return: a list of dictionaries (each dictionary represents one housing post)
    """

    return_lst = []
    db_dest = 'database/' + db_name
    output_message = ''
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()
    where_limit = ''

    if lang == 'zh':
        statement = '''
            SELECT Title, URL, Region, Address, Style, TotalPriceCNY, TotalAreaSqM, UnitPriceCNY
            FROM Houses
            {}
        ;'''
        key_names = ['Title', 'URL', 'Region', 'Address', 'Style', 'TotalPriceCNY', 'TotalAreaSqM', 'UnitPriceCNY']

        if group is None:
            if group_id is None:
                output_message += '全上海'
            else:
                return None

        elif group == 'region':
            region_dict = get_old_region_dict(db_name=db_name, lang=lang)

            region_id_lst = list(region_dict.keys())
            output_message += '区域：'
            if group_id in region_id_lst:
                output_message += region_dict[group_id]
                where_limit = 'WHERE RegionId = {}'.format(group_id)
            else:
                return None

        elif group == 'size_level':
            size_level_dict = get_size_level_dict(db_name=db_name, lang=lang)
            print(size_level_dict)
            size_level_lst = list(size_level_dict.keys())
            output_message += '面积：'
            if group_id in size_level_lst:
                output_message += size_level_dict[group_id]
                where_limit = 'WHERE SizeLevel = {}'.format(group_id)
            else:
                return None

        elif group == 'price_level':
            price_level_dict = get_price_level_dict(db_name=db_name, lang=lang)
            print(price_level_dict)
            price_level_lst = list(price_level_dict.keys())
            output_message += '总价：'
            if group_id in price_level_lst:
                output_message += price_level_dict[group_id]
                where_limit = 'WHERE PriceLevel = {}'.format(group_id)
            else:
                return None

        elif group == 'num_bd':
            style_lst = get_style_lst(db_name)
            print(style_lst)
            output_message += '户型：'
            if group_id in style_lst:
                output_message += str(group_id) + ' 室'
                where_limit = 'WHERE NumOfBd = {}'.format(group_id)
            else:
                return None

        else:
            return None

        result = cur.execute(statement.format(where_limit))
        result_lst = result.fetchall()
        for row in result_lst:
            row_dict = dict(zip(key_names, row))
            return_lst.append(row_dict)

    elif lang == 'en':
        statement = '''
            SELECT URL, RegionsOld.NameEn, NumOfBd, TotalPriceUSD, TotalAreaSqFt, UnitPriceUSD
            FROM Houses
                JOIN RegionsOld
                    ON Houses.RegionId = RegionsOld.Id
            {}
        ;'''
        key_names = ['URL', 'Region', 'NumOfBd', 'TotalPriceUSD', 'TotalAreaSqFt', 'UnitPriceUSD']

        if group is None:
            if group_id is None:
                output_message += 'All in Shanghai'
            else:
                return None

        elif group == 'region':
            region_dict = get_old_region_dict(db_name=db_name, lang=lang)
            print(region_dict)
            region_id_lst = list(region_dict.keys())
            output_message += 'Region: '
            if group_id in region_id_lst:
                output_message += region_dict[group_id]
                where_limit = 'WHERE RegionId = {}'.format(group_id)
            else:
                return None

        elif group == 'size_level':
            size_level_dict = get_size_level_dict(db_name=db_name, lang=lang)
            print(size_level_dict)
            size_level_lst = list(size_level_dict.keys())
            output_message += '面积：'
            if group_id in size_level_lst:
                output_message += size_level_dict[group_id]
                where_limit = 'WHERE SizeLevel = {}'.format(group_id)
            else:
                return None

        elif group == 'price_level':
            price_level_dict = get_price_level_dict(db_name=db_name, lang=lang)
            print(price_level_dict)
            price_level_lst = list(price_level_dict.keys())
            output_message += '总价：'
            if group_id in price_level_lst:
                output_message += price_level_dict[group_id]
                where_limit = 'WHERE PriceLevel = {}'.format(group_id)
            else:
                return None

        elif group == 'num_bd':
            style_lst = get_style_lst(db_name)
            print(style_lst)
            output_message += '户型：'
            if group_id in style_lst:
                output_message += str(group_id) + ' 室'
                where_limit = 'WHERE NumOfBd = {}'.format(group_id)
            else:
                return None

        else:
            return None

        result = cur.execute(statement.format(where_limit))
        result_lst = result.fetchall()
        for row in result_lst:
            row_dict = dict(zip(key_names, row))
            return_lst.append(row_dict)

    else:
        return None

    conn.close()
    return return_lst


if __name__ == '__main__':
    # print(get_old_region_dict(lang='en'))
    # print(get_new_region_dict(lang='en'))
    # print(get_price_level_dict(lang='zh'))
    # print(get_size_level_dict(lang='en'))
    # print(get_avgs(lang='en', data='unit_price', group='size_level'))
    # print(get_new_region_data(lang='en', data='density'))
    # house_post_lst = table_get_housing_posts(lang='en', group='region', group_id=3)
    # if house_post_lst is not None:
    #     print(len(house_post_lst))
    #     print(house_post_lst[0])
    # else:
    #     print('None')
    pass
