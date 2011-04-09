#!/usr/bin/env python
'''
findmissing.py - helps you figure out which photos someone deleted from your memory card

Usage:
$ python findmissing.py /path/to/your/photos
'''

import os
import re
import sys


def scandir(path):
    if not os.path.isdir(path):
        print "'%s' is not a directory!" % path
        return
    
    filename_pattern = re.compile(r"^\w+?(\d+)\.(?:jpg|mpg)$", re.IGNORECASE)
    existent_numbers = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            mo = filename_pattern.match(filename)
            if mo:
                number = int(mo.group(1))
                existent_numbers.append(number)
    
    #print min(existent_numbers), max(existent_numbers)
    #print existent_numbers
    all_numbers = xrange(min(existent_numbers), max(existent_numbers))
    
    missing_numbers = sorted(set(all_numbers).difference(existent_numbers))
    
    if missing_numbers:
        print "Missing (%d):" % len(missing_numbers)
        print "\n".join(str(number) for number in missing_numbers)
    else:
        print "Nothing missing!"

if __name__ == '__main__':
    path = sys.argv[1]
    scandir(path)
    
