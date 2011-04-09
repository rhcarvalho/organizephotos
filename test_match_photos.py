import unittest
from random import sample

from match_photos import match_photos


class TestMatchPhotos(unittest.TestCase):

    def test_match_single_correspondence(self):
        low_res = ['/path/to/low/res/DSC00004.jpg',
                   '/path/to/low/res/DSC00003.jpg']
        hi_res = ['/path/to/hi/res/DSC00000.jpg',
                  '/path/to/hi/res/DSC00001.jpg',
                  '/path/to/hi/res/DSC00002.jpg',
                  '/path/to/hi/res/DSC00003.jpg',
                  '/path/to/hi/res/DSC00004.jpg',
                  '/path/to/hi/res/DSC00005.jpg',
                  '/path/to/hi/res/DSC00006.jpg',
                  '/path/to/hi/res/DSC00007.jpg',
                  '/path/to/hi/res/DSC00008.jpg',
                  '/path/to/hi/res/DSC00009.jpg']
        match = [['/path/to/hi/res/DSC00004.jpg'],
                 ['/path/to/hi/res/DSC00003.jpg']]
        
        self.assertEqual(match_photos(low_res, hi_res), match)

    def test_match_multiple_correspondence(self):
        low_res = ['/path/to/low/res/DSC00003.jpg',
                   '/path/to/low/res/DSC00004.jpg']
        hi_res = ['/path/to/hi/res/DSC00000.jpg',
                  '/path/to/hi/res/DSC00001.jpg',
                  '/path/to/hi/res/DSC00002.jpg',
                  '/path/to/hi/res/DSC00003.jpg',
                  '/path/to/hi/res/DSC00004.jpg',
                  '/path/to/hi/res/DSC00005.jpg',
                  '/path/to/hi/res/DSC00006.jpg',
                  '/path/to/hi/res/DSC00007.jpg',
                  '/path/to/hi/res/DSC00008.jpg',
                  '/path/to/hi/res/DSC00009.jpg',
                  '/path/to/another/hi/res/DSC00004.jpg',
                  '/path/to/another/hi/res/DSC00003.jpg']
        match = [['/path/to/hi/res/DSC00003.jpg',
                  '/path/to/another/hi/res/DSC00003.jpg'],
                 ['/path/to/hi/res/DSC00004.jpg',
                  '/path/to/another/hi/res/DSC00004.jpg']]
        
        self.assertEqual(match_photos(low_res, hi_res), match)

    def test_match_no_correspondence(self):
        low_res = ['/path/to/low/res/DSC00003.jpg',
                   '/path/to/low/res/DSC00004.jpg']
        hi_res = []
        match = [[], []]
        
        self.assertEqual(match_photos(low_res, hi_res), match)

    def test_match_some_correspondence(self):
        low_res = ['/path/to/low/res/DSC00003.jpg',
                   '/path/to/low/res/DSC00004.jpg']
        hi_res = ['/path/to/hi/res/DSC00004.jpg',
                  '/path/to/hi/res/DSC00005.jpg',
                  '/path/to/hi/res/DSC00006.jpg',
                  '/path/to/hi/res/DSC00007.jpg',
                  '/path/to/hi/res/DSC00008.jpg',
                  '/path/to/hi/res/DSC00009.jpg']
        match = [[], ['/path/to/hi/res/DSC00004.jpg']]
        
        self.assertEqual(match_photos(low_res, hi_res), match)

    # ignore this test because it can take some tens of second to run
    def _test_big_input(self):
        _max = 100000
        _common = sample(xrange(_max), 200)
        low_res = ['/path/to/low/res/DSC%05d.jpg' % i for i in _common]
        hi_res = ['/path/to/hi/res/DSC%05d.jpg' % i for i in xrange(_max)]
        match = [['/path/to/hi/res/DSC%05d.jpg' % i] for i in _common]
        
        self.assertEqual(match_photos(low_res, hi_res), match)


if __name__ == '__main__':
    unittest.main()

