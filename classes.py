import csv


class House(object):

    def __init__(self, title, url, info_div):
        info_brick_divs = info_div.find_all(class_="tr-line")

        total_price_div = info_brick_divs[0]
        area_div = info_brick_divs[1]
        address_div = info_brick_divs[3]

        address_detail_divs = address_div.find_all(class_="trl-item2")
        court_div = address_detail_divs[0]
        region_div = address_detail_divs[1]

        self.title = title
        self.url = url

        self.total_price_cny = int(total_price_div.find(class_="trl-item").i.text.strip())
        self.total_price_usd = round(self.total_price_cny * 10000 * 0.16 / 1000)

        self.style = area_div.find(class_="trl-item1 w146").div.text.strip()
        self.num_bedroom = int(self.style[0])

        self.area_sq_m = round(float(area_div.find(class_="trl-item1 w182").div.text.strip().replace('平米', '')), 1)
        self.area_sq_ft = round(self.area_sq_m * 10.7584, 1)

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
