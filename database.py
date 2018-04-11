import sqlite3
import csv
from fetchdata import *

DB_NAME = 'Fang_db.sqlite'


def db_init(db_name):
    """
    There are 4 tables in database Fang_db.sqlite:
        Houses: all housing posts retrieved from Fang.com
        RegionsOld: all regions that used by Fang.com (19 regions)
        RegionsNew: all shanghai districts (16 districts) under new policy (after year 2016)
        Sizes: set several levels for total area of houses
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
        DROP TABLE IF EXISTS Sizes
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
            Region TEXT,
            Address TEXT,
            Style TEXT,
            TotalPriceCNY INT,
            TotalAreaSqM FLOAT,
            UnitPriceCNY INT,
            RegionId INT,
            NumOfBd INT,
            SizeId INT,      
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
        CREATE TABLE IF NOT EXISTS Sizes (
            Id INTEGER PRIMARY KEY,
            SizeRange TEXT
    );'''
    cur.execute(statement)
    conn.commit()

    conn.close()


def insert_houses_data(db_name):
    all_housing_post = get_all_second_hand_housing_sh_Fang()

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for i in all_housing_post:
        statement = "INSERT INTO Houses (Title, Region, Address, Style, TotalPriceCNY, TotalAreaSqM, " \
                    "UnitPriceCNY, NumOfBd, TotalPriceUSD, TotalAreaSqFt, UnitPriceUSD) VALUES (" + "?,"*10 + "?)"
        print(i.title)
        insertion = (i.title, i.region_zh, i.address, i.style, i.total_price_cny, i.area_sq_m, i.unit_price_cny,
                     i.num_bedroom, i.total_price_usd, i.area_sq_ft, i.unit_price_usd)
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


def insert_regions_old_data(db_name):
    pass


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


def insert_sizes_data(db_name):
    pass


if __name__ == '__main__':
    # db_init(DB_NAME)
    # insert_houses_data(DB_NAME)
    # insert_regions_old_data(DB_NAME)
    # insert_regions_new_data(DB_NAME)
    insert_sizes_data(DB_NAME)
