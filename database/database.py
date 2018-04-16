import sqlite3
from fetchdata import *

DB_NAME = 'Fang_db.sqlite'
DB_TEST = 'Fang_db_test.sqlite'


def db_init(db_name):
    """
    There are 4 tables in database Fang_db.sqlite:
        Houses: all housing posts retrieved from Fang.com
        RegionsOld: all regions that used by Fang.com (19 regions)
        RegionsNew: all shanghai districts (16 districts) under new policy (after year 2015)
        SizeLevels: set several levels for total area of houses
        PriceLevels: set several levels for total prices of houses
    """

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS Houses
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS RegionsOld
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS RegionsNew
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS SizeLevels
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS PriceLevels
    '''
    cur.execute(statement)
    conn.commit()

    """
    Table Houses:
        RegionId: Old region categories used by Fang.com (19 regions)
    """
    statement = '''
        CREATE TABLE IF NOT EXISTS Houses (
            Id INTEGER PRIMARY KEY,
            Title TEXT,
            URL TEXT,
            Region TEXT,
            Address TEXT,
            Style TEXT,
            TotalPriceCNY INT,
            TotalAreaSqM FLOAT,
            UnitPriceCNY INT,
            RegionId INT,
            NumOfBd INT,
            PriceLevel INT, 
            SizeLevel INT,
            TotalPriceUSD INT,
            TotalAreaSqFt FLOAT, 
            UnitPriceUSD INT
    );'''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS RegionsOld (
            Id INTEGER PRIMARY KEY,
            NameZh TEXT,
            NameEn TEXT,
            NewNameZh TEXT,
            NewNameEn TEXT,
            NewRegionId INT
    );'''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS RegionsNew (
            Id INTEGER PRIMARY KEY,
            NameZh TEXT,
            NameEn TEXT,
            DistrictCode INT,
            AreaSqKm FLOAT,
            Population10K FLOAT,
            Density10KSqKm FLOAT,
            GDP100MMCNY FLOAT,
            GDPPerCapita10KCNY FLOAT,
            AreaSqMi FLOAT,
            PopulationMM FLOAT,
            DensityKSqMi FLOAT,
            GDPBUSD FLOAT,
            GDPPerCapitaKUSD FLOAT
    );'''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS SizeLevels (
            Id INTEGER PRIMARY KEY,
            SizeRange TEXT
    );'''
    cur.execute(statement)

    statement = '''
        CREATE TABLE IF NOT EXISTS PriceLevels (
            Id INTEGER PRIMARY KEY,
            PriceRange TEXT
    );'''
    cur.execute(statement)
    conn.commit()

    conn.close()


def insert_houses_data(db_name, house_lst):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for i in house_lst:
        statement = "INSERT INTO Houses (Title, URL, Region, Address, Style, TotalPriceCNY, TotalAreaSqM, " \
                    "UnitPriceCNY, NumOfBd, PriceLevel, SizeLevel, TotalPriceUSD, TotalAreaSqFt, UnitPriceUSD) " \
                    "VALUES (" + "?,"*13 + "?)"
        insertion = (i.title, i.url, i.region_zh, i.address, i.style, i.total_price_cny, i.area_sq_m, i.unit_price_cny,
                     i.num_bedroom, i.price_level, i.size_level, i.total_price_usd, i.area_sq_ft, i.unit_price_usd)
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


def insert_regions_old_data(db_name):
    infile = open('csv/sh_regions_Fang.csv')
    content = list(csv.reader(infile))[1:]

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for row in content:
        statement = 'INSERT INTO RegionsOld (NameZh, NameEn, NewNameZh, NewNameEn) ' \
                    'VALUES (?,?,?,?)'
        cur.execute(statement, row)

    conn.commit()
    conn.close()


def insert_regions_new_data(db_name):
    infile = open('csv/sh_regions_new.csv')
    content = list(csv.reader(infile))[1:17]

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for row in content:
        statement = 'INSERT INTO RegionsNew VALUES (' + '?,'*13 + '?)'
        insertion = [None] + row
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


def insert_size_levels_data(db_name):

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    size_levels_dict = {
        1: '300平米及以上',
        2: '150-299.99平米',
        3: '110-149.99平米',
        4: '70-109.99平米',
        5: '70平米以下（不包含70平米）'
    }
    for i in range(1, 6):
        statement = '''
            INSERT INTO SizeLevels VALUES (?,?)
        '''
        insertion = (i, size_levels_dict[i])
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


def insert_price_levels_data(db_name):

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    price_levels_dict = {
        1: '3000万及以上',
        2: '1000-2999.99万',
        3: '500-999.99万',
        4: '200-499.99万',
        5: '200万以下（不包含200万）'
    }
    for i in range(1, 6):
        statement = '''
            INSERT INTO PriceLevels VALUES (?,?)
        '''
        insertion = (i, price_levels_dict[i])
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


def update_houses_regionId(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        UPDATE Houses
        SET RegionId = (
            SELECT Id FROM RegionsOld
            WHERE Houses.Region = RegionsOld.NameZh
        )
    ;'''
    cur.execute(statement)
    conn.commit()
    conn.close()


def update_regions_old_newId(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        UPDATE RegionsOld
        SET NewRegionId = (
            SELECT Id FROM RegionsNew
            WHERE RegionsOld.NewNameZh = RegionsNew.NameZh
        )
    ;'''
    cur.execute(statement)

    statement = '''
        UPDATE RegionsOld
        SET NewRegionId = 17
        WHERE RegionsOld.NewNameZh = \'上海周边\'
    ;'''
    cur.execute(statement)

    conn.commit()
    conn.close()


def db_test(db_name=DB_TEST):
    db_init(db_name)
    first_page_housing_post = get_first_page_second_hand_housing_sh_Fang(CACHE_FNAME_WHOLE, CACHE_FNAME_INDIVIDUAL)
    insert_houses_data(db_name, first_page_housing_post)
    insert_regions_old_data(db_name)
    insert_regions_new_data(db_name)
    insert_size_levels_data(db_name)
    insert_price_levels_data(db_name)
    update_houses_regionId(db_name)
    update_regions_old_newId(db_name)


def db_main(db_name=DB_NAME):
    db_init(db_name)
    all_housing_post = get_all_second_hand_housing_sh_Fang(CACHE_FNAME_WHOLE, CACHE_FNAME_INDIVIDUAL)
    insert_houses_data(db_name, all_housing_post)
    insert_regions_old_data(db_name)
    insert_regions_new_data(db_name)
    insert_size_levels_data(db_name)
    insert_price_levels_data(db_name)
    update_houses_regionId(db_name)
    update_regions_old_newId(db_name)


if __name__ == '__main__':

    while True:
        message = '''
    Database exists. Do you want to rebuild database?(y/n)
    '''
        option = input(message)
        if option.strip().lower() == 'y':
            message = '''
    Do you want to rebuild a TEST database or COMPLETE one?(t/c)

    NOTICE: There would be 30 records in test database and 2855 in complete one.
            If you want to rebuild a complete database, it might take a lot of time to complete the process.
            '''
            option_sub = input(message)
            while True:
                if option_sub.strip().lower() == 't':
                    db_test()
                    break
                elif option_sub.strip().lower() == 'c':
                    db_main()
                    break
                else:
                    print('Invaid input, please try again.\n')
                    continue
            break                    
        elif option.strip().lower() == 'n':
            break
        else:
            print('Invaid input, please try again.\n')
            continue
