import csv
import json


class House(object):

    def __init__(self, title, house_url, info_div):
        info_brick_divs = info_div.find_all(class_="tr-line")

        total_price_div = info_brick_divs[0]
        area_div = info_brick_divs[1]
        address_div = info_brick_divs[3]

        address_detail_divs = address_div.find_all(class_="trl-item2")
        court_div = address_detail_divs[0]
        region_div = address_detail_divs[1]

        self.title = title
        self.url = house_url

        self.total_price_cny = int(total_price_div.find(class_="trl-item").i.text.strip())
        self.total_price_usd = round(self.total_price_cny * 10000 * 0.16 / 1000)
        if self.total_price_cny >= 3000:
            self.price_level = 1
        elif self.total_price_cny >= 1000:
            self.price_level = 2
        elif self.total_price_cny >= 500:
            self.price_level = 3
        elif self.total_price_cny >= 200:
            self.price_level = 4
        else:
            self.price_level = 5

        self.style = area_div.find(class_="trl-item1 w146").div.text.strip()
        self.num_bedroom = int(self.style[0])

        self.area_sq_m = round(float(area_div.find(class_="trl-item1 w182").div.text.strip().replace('平米', '')), 1)
        self.area_sq_ft = round(self.area_sq_m * 10.7584, 1)
        if self.area_sq_m >= 300:
            self.size_level = 1
        elif self.area_sq_m >= 150:
            self.size_level = 2
        elif self.area_sq_m >= 110:
            self.size_level = 3
        elif self.area_sq_m >= 70:
            self.size_level = 4
        else:
            self.size_level = 5

        self.unit_price_cny = int(area_div.find(class_="trl-item1 w132").div.text.strip().replace('元/平米', ''))
        self.unit_price_usd = round(self.total_price_usd * 1000 / self.area_sq_ft)

        self.address = court_div.find(class_="rcont").a.text.strip()
        self.region_zh = region_div.find(class_="rcont").a.text.strip()

        region_dict = {}
        infile = open('csv/sh_regions_Fang.csv', 'r')
        infile_content = list(csv.reader(infile))
        for row in infile_content[1:]:
            region_dict[row[0]] = row[1]
        self.region_en = region_dict[self.region_zh]

    def cache_house_object(self, cache_fname_house_object):
        unique_identifier = self.url
        cache_fdest = 'cache/' + cache_fname_house_object

        try:
            infile = open(cache_fdest, 'r')
            infile_content = infile.read()
            diction = json.loads(infile_content)
            infile.close()
        except Exception:
            diction = {}

        if unique_identifier in diction:
            print('This House object has been cached...')
            content_dict = diction[unique_identifier]
        else:
            print('Cache new House object...')
            content_dict = {}

            content_dict['title'] = self.title
            content_dict['total_price_cny'] = self.total_price_cny
            content_dict['total_price_usd'] = self.total_price_usd
            content_dict['price_level'] = self.price_level
            content_dict['style'] = self.style
            content_dict['num_bedroom'] = self.num_bedroom
            content_dict['area_sq_m'] = self.area_sq_m
            content_dict['area_sq_ft'] = self.area_sq_ft
            content_dict['size_level'] = self.size_level
            content_dict['unit_price_cny'] = self.unit_price_cny
            content_dict['unit_price_usd'] = self.unit_price_usd
            content_dict['address'] = self.address
            content_dict['region_zh'] = self.region_zh
            content_dict['region_en'] = self.region_en

            diction[unique_identifier] = content_dict
            dumped_dict = json.dumps(diction, indent=2)
            outfile = open(cache_fdest, 'w')
            outfile.write(dumped_dict)
            outfile.close()
        return content_dict

    def __str__(self):
        total_price_str = str(self.total_price_cny) + ' 万'

        output = '''
            标题: {}
            小区: {}
            区域: {:<10}\t\t| Region: {}     
            总价: {:<10}\t\t| Total Price: {} K USD
            户型: {}\t\t\t| Number of Bedrooms: {}
            建筑面积: {} 平米\t\t| Area: {} SQ FT 
            单价: {} 元/平米\t\t| Unit Price: {} USD PER SQ FT
        '''.format(self.title, self.address, self.region_zh, self.region_en, total_price_str, self.total_price_usd,
                   self.style, self.num_bedroom, self.area_sq_m, self.area_sq_ft, self.unit_price_cny,
                   self.unit_price_usd)
        return output
