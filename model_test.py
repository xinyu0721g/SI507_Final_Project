import unittest
from model import *


class TestModel(unittest.TestCase):

    def test_get_avgs(self):
        dict1 = get_avgs(db_name=DB_TEST, lang='zh')
        self.assertEqual(dict1[0], 68848.5)

        dict2 = get_avgs(db_name=DB_TEST, lang='zh', data='unit_price', group='region')
        self.assertEqual(dict2[12], 126636.83)
        self.assertLessEqual(len(dict2), 17)

        dict3 = get_avgs(db_name=DB_TEST, lang='zh', data='unit_price', group='price_level')
        self.assertEqual(dict3[1], 143185.75)
        self.assertLessEqual(len(dict3), 5)

        dict4 = get_avgs(db_name=DB_TEST, lang='zh', data='unit_price', group='size_level')
        self.assertEqual(dict4[3], 69823.5)
        self.assertLessEqual(len(dict4), 5)

        dict5 = get_avgs(db_name=DB_TEST, lang='en', data='total_price', group='size_level')
        self.assertEqual(dict5[2], 3762.36)
        self.assertLessEqual(len(dict5), 5)

        dict6 = get_avgs(db_name=DB_TEST, lang='en', data='unit_price', group='num_bd')
        self.assertEqual(dict6[2], 803.15)
        self.assertLessEqual(len(dict6), 5)

    def test_get_region_data(self):
        dict1 = get_new_region_data(lang='zh')
        self.assertEqual(dict1[10], 3.24)

        dict2 = get_new_region_data(data='gdp_per_capita')
        self.assertIsNone(dict2)

        dict3 = get_new_region_data(lang='zh', data='gdp')
        self.assertEqual(dict3[12], 30.77)
        self.assertEqual(dict3[11], 15.57)


unittest.main()
