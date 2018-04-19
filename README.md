# SI507 Final Project - Xinyu Yan

This project creates a Flask app where users can search for basic information of second-hand housing markets in Shanghai, China. Both English and Chinese languages are supported.
<br>

## Acknowledgement
First of all, I would like to show my great gratitude to [Tongyan Xu](https://github.com/TongyanX) who offered me a lot of help with my project, especially building html templates (dataTable, javascript, css, etc.).

## How To Use

### Option1: Heroku app [LINK](https://blooming-lowlands-79795.herokuapp.com/)

### Option2: Run at Terminal

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Data Sources

### Fang.com  **<HTML**>

**Name:** Fang.com

**URL:** http://sh.fang.com/

**Web Scraping and Crawling:**
- Using next page extend to get access to next page (99 times, 100 pages in total)
- Using individual housing post extend to get access to individual housing post page (100*30=3000 times, 3000 posts in total)
- Number of pages scraped: 100+100*30 = 3100

**Challenge score:** 8

## Class Definition

### House

**Instance:** each House instance represents a housing post on Fang.com

**Attributes:**
- title: title of housing post
- url: url of housing post
- total_prices_cny: total price of the house in CNY
- total_price_usd: total price of the house in USD
- price_level: price level for total price in CNY (5 levels in total)
- style: style of the house
- num_bedroom: number of bedrooms
- area_sq_m: total area of the house in square meters
- area_sq_ft: total area of the house in square feet
- size_level: size level for total area in square meters (5 levels in total)
- unit_price_cny: unit price of the house in CNY
- unit_price_usd: unit price of the house in USD
- address: address of the house (court/garden name)
- region_en: region name in English (traditional region division of Shanghai)

**Methods:**
- __str__: return a string output of basic information of a housing post

## Data Access and Storage

### Database description

**Name:** Fang_db.sqlite, Fang_db_test.sqlite

**Tables:**
- Houses
- RegionsOld
- RegionsNew
- PriceLevels
- SizeLevels

**Links Between Tables:**
- Houses
    - Houses.RegionId (Foreign key): RegionsOld.Id (Primary key)
    - Houses.PriceLevel (Foreign key): PriceLevels.Id (Primary key)
    - Houses.SizeLevel (Foreign key): SizeLevels.Id (Primary key)
- RegionsOld
    - RegionsOld.NewRegionId (Foreign key): RegionsNew.Id (Primary key)

### Rebuild database

**step1** cd to database folder

**step2** run database.py
- you would have two options: rebuild database or not
- if you choose rebuild database, there would be two following options:
    - rebuild a test database: this would rebuild a database including 30 records of housing posts on the first page of Fang.com
    - rebuild a complete database: this would rebuild a database including all 2855 records of housing posts on all pages of Fang.com (WARNING: This process might take A LOT OF time!)

### Unit Testing
- There is a separate test file called database_test.py in database folder
- This test file tests whether tables in database are correctly built and tables are correctly linked to each other
- 2 test cases and 5 assertions

## Data Processing

### Main functions

### get_avgs (db_name=DB_TEST, lang='zh', data='unit_price', group=None)

get average total_price/total_area/unit_price for each group (if group=None, get data for all posts)

**parameters:**
- db_name: database name
- lang: language, default Chinese (options: zh(Chinese)/en(English))
- data: returned data column, default unit_price (options: total_price/total_area/unit_price)
- group: group method default None (options: None/region/num_bd/size_level/price_level)

**return:** a dictionary where key is group name and value is correlated average total_price/total_area/unit_price

**sample output:**

```
print(get_avgs(lang='en', data='unit_price', group='size_level'))
```
```
{1: 1591.77, 2: 1136.36, 3: 889.92, 5: 739.44, 4: 699.76}
```

### get_new_region_data(db_name=DB_NAME, lang='en', data='density')

get region information from RegionsNew table

**parameters:**
- db_name: database name, default DB_NAME
- lang: language, default English (options: zh(Chinese)/en(English))
- data: returned data column, default density (options: density/gdp(per capita))

**return:** a dictionary where key is region id and value is correlated density/gdp(per capita)

**sample output:**
```
print(get_new_region_data(lang='en', data='density'))
```
```
{10: 83.91, 12: 82.9, 11: 74.01, 5: 60.08, 7: 56.2, 3: 51.35, 6: 46.73, 4: 17.84, 2: 17.68, 1: 12.29, 9: 8.81, 8: 7.56, 13: 4.66, 14: 4.4, 15: 3.37, 16: 1.23}
```

### table_get_housing_posts(db_name=DB_NAME, lang='zh', group=None, group_id=None)
get a list of house info dictionaries by group

**parameters:**
- db_name: database name, default DB_NAME
- lang: language, default English (options: zh(Chinese)/en(English))
- group: group method, default None (options: None/region/num_bd/size_level/price_level)
- group_id: region_id/num_bd/size_level/price_level

**return:** a list of dictionaries (each dictionary represents one housing post)

**sample output:**

```
house_post_lst = table_get_housing_posts(lang='en', group='region', group_id=3)
if house_post_lst is not None:
    print(len(house_post_lst))
    print(house_post_lst[0])
else:
    print('None')
```
```
150
{'URL': 'http://esf.sh.fang.com/chushou/3_317130242.htm', 'Region': 'Xuhui District', 'NumOfBd': 3, 'TotalPriceUSD': 1856, 'TotalAreaSqFt': 1386.8, 'UnitPriceUSD': 1338}

```

### Unit Testing
- Test the functionality of functions in model.py
- 2 test case and 15 assertions

## Data Presentation

### Flask app (6 web pages in total)
There are three main pages and each page is supported both in English and Chinese.

**index page**
Welcome page, user can be redirected to search/chart pages through buttons at page bottom or change to Chinese language.

**search page**
User can search for housing posts in any region in Shanghai.

**chart page**
User can plot bar chart or scatter chart to get a general view of Shanghai second-hand housing market.

## Author

* **Xinyu Yan** - [xinyu0721g](https://github.com/xinyu0721g)
