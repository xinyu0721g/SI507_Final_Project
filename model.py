import sqlite3

DB_NAME = 'Fang_db.sqlite'
DB_TEST = 'Fang_db_test.sqlite'


def get_avg_by_group(db_name=DB_TEST, lang='zh', data='unit_price', group=None):
    """
    get average total_price/total_area/unit_price for each group (if group=None, get data for all posts)
    :param db_name: database name
    :param lang: language, default Chinese (options: zh(Chinese)/en(English))
    :param data: returned data column, default unit_price (options: total_price/total_area/unit_price)
    :param group: group method default None (options: None/region/num_bd/size_level/price_level)
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
            output_message += '：平均总面积（平米）'
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
        return_dict['all'] = round(value, 2)
        if lang == 'zh':
            output_message = '全上海' + output_message
        else:
            output_message = 'All in Shanghai' + output_message
    elif group == 'region':
        if lang == 'zh':
            select_group = 'RegionsOld.NewNameZh'
            output_message = '区域' + output_message
        else:
            select_group = 'RegionsOld.NewNameEn'
            output_message = 'Region' + output_message
        statement = '''
            SELECT {}, {}
            FROM Houses
                JOIN RegionsOld
                    ON Houses.RegionId = RegionsOld.Id
            GROUP BY RegionsOld.NewRegionId
            ORDER BY {} DESC
        ;'''.format(select_group, data_column, data_column)
        result = cur.execute(statement)
        result_lst = result.fetchall()
        for (new_region_name, value) in result_lst:
            return_dict[new_region_name] = round(value, 2)
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

    print('\n{' + output_message+'}')
    return return_dict


def get_region_data(db_name=DB_TEST, lang='zh', data='density'):
    """
    get region information from RegionsNew table
    :param db_name: database name
    :param lang: language, default Chinese
    :param data: returned data column, default density (options: density/gdp_per_capita)
    :return: a dictionary where key is region name and value is correlated density/gdp_per_capita
    """
    return_dict = {}
    db_dest = 'database/' + db_name
    output_message = ''

    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        region_column = 'NameZh'
        output_message += '区域：'
        if data == 'density':
            data_column = 'Density10KSqKm'
            output_message += '人口密度（万人/平方公里）'
        elif data == 'gdp_per_capita':
            data_column = 'GDPPerCapita10KCNY'
            output_message += '人均GDP（万元）'
        else:
            return None
    elif lang == 'en':
        region_column = 'NameEn'
        output_message += 'Region: '
        if data == 'density':
            data_column = 'DensityKSqMi'
            output_message += 'Density (K/Sq Mi)'
        elif data == 'gdp_per_capita':
            data_column = 'GDP Per Capita (K USD)'
        else:
            return None
    else:
        return None

    statement = '''
        SELECT {}, {} 
        FROM RegionsNew
        ORDER BY {} DESC
    ;'''.format(region_column, data_column, data_column)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (region_name, data_column) in result_lst:
        return_dict[region_name] = data_column

    conn.close()

    print('\n{' + output_message+'}')
    return return_dict


def get_old_region_lst(db_name=DB_TEST, lang='zh'):
    region_lst = []
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
        SELECT {}
        FROM RegionsOld
    ;'''.format(select_col)
    result = cur.execute(statement)
    result_lst = result.fetchall()
    for (region_name,) in result_lst:
        region_lst.append(region_name)

    conn.close()
    return region_lst


def get_house_info_by_group(db_name=DB_TEST, lang='zh', group=None, group_name=None):
    return_lst = []
    db_dest = 'database/' + db_name
    output_message = ''
    conn = sqlite3.connect(db_dest)
    cur = conn.cursor()

    if lang == 'zh':
        region_lst = get_old_region_lst(db_name, lang='zh')
        print(region_lst)
        statement = '''
            SELECT Title, URL, Region, Address, Style, TotalPriceCNY, TotalAreaSqM, UnitPriceCNY
            FROM Houses
            {}
        ;'''
        if group is None:
            where_limit = ''
            output_message += '全上海'
            result = cur.execute(statement.format(where_limit))
            return_lst = result.fetchall()
        elif group == 'region':
            output_message += '区域：'
            if group_name in region_lst:
                output_message += group_name
                where_limit = 'WHERE Region = \'{}\''.format(group_name)
                result = cur.execute(statement.format(where_limit))
                return_lst = result.fetchall()
            else:
                return None
        elif group == 'size_level':
            output_message += '面积：'
            if group_name in [1, 2, 3, 4, 5]:
                statement_sub = '''
                    SELECT SizeRange
                    FROM SizeLevels 
                    WHERE Id = {}
                ;'''.format(group_name)
                size_range = cur.execute(statement_sub).fetchone()
                output_message += size_range
                where_limit = 'WHERE SizeLevel = {}'.format(group_name)
                result = cur.execute(statement.format(where_limit))
                return_lst = result.fetchall()
        elif group == 'price_level':
            output_message += '总价：'
            if group_name in [1, 2, 3, 4, 5]:
                statement_sub = '''
                    SELECT PriceRange
                    FROM PriceLevels 
                    WHERE Id = {}
                ;'''.format(group_name)
                price_range = cur.execute(statement_sub).fetchone()
                output_message += price_range
                where_limit = 'WHERE PriceLevel = {}'.format(group_name)
                result = cur.execute(statement.format(where_limit))
                return_lst = result.fetchall()
        else:
            return None

    elif lang == 'en':
        region_lst = get_old_region_lst(db_name, lang='en')
        print(region_lst)
        statement = '''
            SELECT URL, RegionsOld.NameEn, NumOfBd, TotalPriceUSD, TotalAreaSqFt, UnitPriceUSD
            FROM Houses
                JOIN RegionsOld
                    ON Houses.RegionId = RegionsOld.Id
            {}
        ;'''
        if group is None:
            where_limit = ''
            output_message += 'All in Shanghai'
            result = cur.execute(statement.format(where_limit))
            return_lst = result.fetchall()
        elif group == 'region':
            output_message += 'Region: '
            if group_name in region_lst:
                output_message += group_name
                where_limit = 'WHERE RegionsOld.NameEn = \'{}\''.format(group_name)
                result = cur.execute(statement.format(where_limit))
                return_lst = result.fetchall()
            else:
                return None
        else:
            return None
    else:
        return None

    conn.close()
    return return_lst


if __name__ == '__main__':
    result = get_house_info_by_group(lang='zh', group='region', group_name='黄浦')
    if result is None:
        print('None')
    else:
        for i in result:
            print(i)
    pass
