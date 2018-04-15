import unittest
from database import *


class TestDatabase(unittest.TestCase):

    def test_houses_table(self):
        conn = sqlite3.connect(DB_TEST)
        cur = conn.cursor()

        sql = '''
        SELECT DISTINCT RegionId FROM Houses
        ;'''
        result = cur.execute(sql)
        region_num = len(result.fetchall())
        self.assertLessEqual(region_num, 19)

        sql = '''
        SELECT TotalPriceCNY, TotalAreaSqM, UnitPriceCNY
        FROM Houses 
        WHERE RegionId = 1
        ORDER BY Id
        ;'''
        result = cur.execute(sql)
        result_list = result.fetchall()
        self.assertEqual(len(result_list), 8)
        self.assertEqual(result_list[0][0], 1480)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DB_TEST)
        cur = conn.cursor()

        sql = '''
        SELECT RegionsNew.NameZh
        FROM Houses
            JOIN RegionsOld 
                ON Houses.RegionId = RegionsOld.Id
            JOIN RegionsNew
                ON RegionsOld.NewRegionId = RegionsNew.Id
        WHERE Houses.Region = \'闸北\'
        '''
        result = cur.execute(sql)
        self.assertEqual(result.fetchone()[0], '静安')

        sql = '''
        SELECT RegionsNew.NameZh
        FROM Houses
            JOIN RegionsOld 
                ON Houses.RegionId = RegionsOld.Id
            JOIN RegionsNew
                ON RegionsOld.NewRegionId = RegionsNew.Id
        WHERE Houses.Region = \'卢湾\'
        '''
        result = cur.execute(sql)
        self.assertEqual(result.fetchone()[0], '黄浦')


unittest.main()
