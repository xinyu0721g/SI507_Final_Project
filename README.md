# SI507 Final Project - Xinyu Yan

This project creates a Flask app where users can search for basic information of second-hand housing markets in Shanghai, China. Both English and Chinese languages are supported.
<br>

## acknowledgement
First of all, I would like to show my great gratitude to [Tongyan Xu](https://github.com/TongyanX) who offered a lot of help with my project, especially building html templates (dataTable, javascript, etc.).

## Data Sources

### Fang.com **<HTML**>**

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

**Method:**
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

**Table links:**
- Houses
    - Houses.RegionId (Foreign): RegionsOld.Id (Primary)
    - Houses.PriceLevel (Foreign): PriceLevels.Id (Primary)
    - Houses.SizeLevel (Foreign): SizeLevels.Id (Primary)
- RegionsOld
    - RegionsOld.NewRegionId (Foreign): RegionsNew.Id (Primary)

### Rebuild database

**step1** cd to database folder

**step2** run database.py
- you would have two options: rebuild database or not
- if you choose rebuild database, there would be two following options:
    - rebuild a test database: this would rebuild a database including 30 records of housing posts on the first page of Fang.com
    - rebuild a complete database: this would rebuild a database including all 2855 records of housing posts on all pages of Fang.com (WARNING: This process might take A LOT OF time!

### Unit Testing
- There is a separate test file called database_test.py in database folder
- This test file tests whether tables in database are correctly built and tables are correctly linked to each other
- 2 test cases and 5 assertions

## Data Processing

### Main functions

**get_avg_by_group**(db_name=DB_TEST, lang='zh', data='unit_price', group=None)

get average total_price/total_area/unit_price for each group (if group=None, get data for all posts)

**parameters:**
- db_name: database name
- lang: language, default Chinese (options: zh(Chinese)/en(English))
- data: returned data column, default unit_price (options: total_price/total_area/unit_price)
- group: group method default None (options: None/region/num_bd/size_level/price_level)

**return:** a dictionary where key is group name and value is correlated average total_price/total_area/unit_price

### Unit Testing
- Test the functionality of functions in model.py
- 2 test case and 15 assertions

## Data Presentation



## Author

* **Xinyu Yan** - [xinyu0721g](https://github.com/xinyu0721g)
