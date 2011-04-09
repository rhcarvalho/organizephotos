# Rodolfo Carvalho - 20011/04/09
# this should be part of http://launchpad.net/organizephotos/

import os


class Photo(object):
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        
    def __eq__(self, other):
        return self.filename == other.filename
        
    def __hash__(self):
        return hash(self.filename)
        
    def __repr__(self):
        return '<Photo@%s>' % self.path


def match_photos(low_resolution_paths, high_resolution_paths):
    low_resolution_photos = set((Photo(path) for path in low_resolution_paths))
    high_resolution_photos = set((Photo(path) for path in high_resolution_paths))
    
    return sorted(photo.path for photo in high_resolution_photos.intersection(low_resolution_photos))


#---------------------------------------------------------------------------------------------

import unittest
from random import sample


class TestMatchPhotos(unittest.TestCase):
    _max = 5000
    _common = sorted(sample(xrange(_max), 2))
    low_res = ['/path/to/low/res/DSC%05d.jpg' % i for i in _common]
    
    hi_res = ['/path/to/hi/res/DSC%05d.jpg' % i for i in xrange(_max)]
    hi_res_match = ['/path/to/hi/res/DSC%05d.jpg' % i for i in _common]

    def test_match_low_high(self):
        self.assertEqual(match_photos(self.low_res, self.hi_res), self.hi_res_match)

if __name__ == '__main__':
    unittest.main()
