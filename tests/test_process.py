#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

import unittest
from pytvname import process

class NormalizeTest(unittest.TestCase):
    """Tests for normalize function"""
    def test_scandal_2009(self):
        self.assertEqual(process.normalize('scandal (2009)'), 'Scandal')

    def test_the_mentalist(self):
        self.assertEqual(process.normalize('[www.down.org]the.mentalist'), 'The Mentalist')

    def test_arrow_us_720p(self):
        self.assertEqual(process.normalize('arrow.us.720p'), 'Arrow')

class InfoTest(unittest.TestCase):
    """Tests for retrive informations function"""
    def test_banshee_s03e07_killers(self):
        result = {
            'showName': 'Banshee',
            'seasonNum': '03',
            'episodeNum': '07',
            'teamName': 'KILLERS',
            'quality': 'HDTV'
        }
        self.assertEqual(process.info('Banshee.S03e07.HDTV.x264-KILLERS[ettv]'), result)

    def test_vikings_s01e01_webdl(self):
        result = {
            'showName': 'Vikings',
            'seasonNum': '01',
            'episodeNum': '01',
            'teamName': 'WEB DL',
            'quality': ''
        }
        self.assertEqual(process.info('vikings 01x01.web.dl'), result)

    def test_the_big_bang_theory_8x16_hdtv_x264_lol(self):
        result = {
            'showName': 'The Big Bang Theory',
            'seasonNum': '08',
            'episodeNum': '16',
            'teamName': 'LOL',
            'quality': 'HDTV'
        }
        self.assertEqual(process.info('The.Big.Bang.Theory.8x16.HDTV.x264-LOL'), result)   

    def test_the_big_bang_theory_816_hdtv_x264_lol(self):
        self.assertEqual(process.info('The.Big.Bang.Theory.816.HDTV.x264-LOL'), None)   

class ApplyFuncsTest(unittest.TestCase):
    """Tests for apply string functions function"""
    def test_house_of_cards_upper(self):
        self.assertEqual(process.applyfuncs('house of cards', ['upper']), 'HOUSE OF CARDS')

    def test_the_big_bang_theory_title(self):
        self.assertEqual(process.applyfuncs('The BIG bang ThEoRy', ['title']), 'The Big Bang Theory')

    def test_the_mentalist_lower_title(self):
        self.assertEqual(process.applyfuncs('The Mentalist', ['lower', 'title']), 'The Mentalist')

    def test_09_zfone(self):
        self.assertEqual(process.applyfuncs('09', ['zfone']), '9')

    def test_5_zftwo(self):
        self.assertEqual(process.applyfuncs('5', ['zftwo']), '05')

class PrcTest(unittest.TestCase):
    """Tests for name processment"""
    def test_banshee_s03e07_killers(self):
        original  = 'Banshee.S03E07.HDTV.x264-KILLERS[ettv]'
        processed = process.prc(original)
        self.assertEqual(processed, 'Banshee S03E07 KILLERS')

    def test_vikings_s01e01_webdl(self):
        original  = 'vikings.s01e01.rites.of.passage.720p.web.dl.sujaidr'
        processed = process.prc(original, '{showName} S{seasonNum}E{episodeNum} {quality} {teamName}')
        self.assertEqual(processed, 'Vikings S01E01 720p WEB DL')

    def test_banshee_s03e08_killers(self):
        original  = 'Banshee.S03E08.HDTV.x264-KILLERS[ettv]'
        processed = process.prc(original, '{showName.lower}.{seasonNum.zfone}{episodeNum}.{teamName.lower}')
        self.assertEqual(processed, 'banshee.308.killers')

    def test_banshee_308_killers(self):
        original  = 'Banshee.308.HDTV.x264-KILLERS[ettv]'
        processed = process.prc(original)
        self.assertEqual(processed, None)

if __name__ == '__main__':
    unittest.main()