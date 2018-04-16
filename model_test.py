import unittest
from model import *


class TestModel(unittest.TestCase):

    def test_get_avg_by_group(self):
        dict1 = get_avg_by_group()
        self.assertEqual(dict1['all'], 68848.5)

        dict2 = get_avg_by_group(lang='zh', data='unit_price', group='region')
        self.assertEqual(dict2['黄浦'], 126636.83)
        self.assertLessEqual(len(dict2), 17)

        dict3 = get_avg_by_group(lang='zh', data='unit_price', group='price_level')
        self.assertEqual(dict3[1], 143185.75)
        self.assertLessEqual(len(dict3), 5)

        dict4 = get_avg_by_group(lang='zh', data='unit_price', group='size_level')
        self.assertEqual(dict4[3], 69823.5)
        self.assertLessEqual(len(dict4), 5)

        dict5 = get_avg_by_group(lang='en', data='total_price', group='size_level')
        self.assertEqual(dict5[2], 3762.36)
        self.assertLessEqual(len(dict5), 5)

        dict6 = get_avg_by_group(lang='en', data='unit_price', group='num_bd')
        self.assertEqual(dict6[2], 803.15)
        self.assertLessEqual(len(dict6), 5)

    def test_get_region_data(self):
        dict1 = get_region_data()
        self.assertEqual(dict1['虹口'], 3.24)

        dict2 = get_region_data(data='gdp')
        self.assertIsNone(dict2)

        dict3 = get_region_data(data='gdp_per_capita')
        self.assertEqual(dict3['黄浦'], 30.77)
        self.assertEqual(dict3['静安'], 15.57)


unittest.main()
