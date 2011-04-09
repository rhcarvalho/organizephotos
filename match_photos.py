# Rodolfo Carvalho - 20011/04/09
# this should be part of http://launchpad.net/organizephotos/

from collections import defaultdict
from os import listdir
from os.path import basename, join
import sys


def match_photos(source_paths, destination_paths):
    '''Find files in `destination_paths` with the same name as of the files
    in `source_paths`.'''
    source_names = (basename(path) for path in source_paths)
    destination_matchs = defaultdict(list)
    for path in destination_paths:
        destination_matchs[basename(path)].append(path)
    return (destination_matchs[name] for name in source_names)
    
def main():
    '''Basic implementation of a main function.
    
    Currently it simply lists the directories FROM and TO, not checking file
    types and not recursing the tree.'''
    
    # Check if the script was called with the right number of arguments
    if len(sys.argv) != 3:
        print >>sys.stderr, "Usage: %s FROM TO" % sys.argv[0]
        sys.exit(1)
    
    # List the directories. This part should be improved to recurse the tree
    # and maybe filter only .jpg files.
    src, dest = map(listdir, sys.argv[1:])
    
    for match in match_photos(src, dest):
        # Ignore empty matches. Maybe we should tell the user that there were
        # no correspondence found for some files.
        if match:
            # Since os.listdir remove path information, it is joined back before
            # printing.
            print ', '.join(join(sys.argv[2], path) for path in match)

#-------------------------------------------------------------------------------

import unittest
from random import sample


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

    def _test_big_input(self):
        _max = 100000
        _common = sample(xrange(_max), 200)
        low_res = ['/path/to/low/res/DSC%05d.jpg' % i for i in _common]
        hi_res = ['/path/to/hi/res/DSC%05d.jpg' % i for i in xrange(_max)]
        match = [['/path/to/hi/res/DSC%05d.jpg' % i] for i in _common]
        
        self.assertEqual(match_photos(low_res, hi_res), match)

if __name__ == '__main__':
#    unittest.main()
    main()
