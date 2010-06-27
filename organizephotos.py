#!/usr/bin/env python
'''
organizephotos.py - organize your photos in directories by date

Usage:
$ python organizephotos.py /path/to/your/photos
'''

import datetime
import os
import re
import sys

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    _using_exif = True
except ImportError:
    _using_exif = False


if _using_exif:
    def _get_exif(filename):
        '''Returns a dictionary with all the EXIF info of a given image.
        '''
        i = Image.open(filename)
        info = i._getexif() or dict()
        return dict([(TAGS.get(tag, tag), value) for tag, value in info.items()])
    
    def _get_exif_date(filename):
        '''Returns the date when the picture was taken.
        
        If the 'DateTime' tag is present in the EXIF info, returns
        the date as YYYY-MM-DD, else returns None.
        '''
        exif = _get_exif(filename)
        date = exif.get('DateTime', '')[:10].replace(':', '-')
        return date


def _get_modification_date(filename):
    '''Returns the modification time of `filename` as YYYY-MM-DD.
    '''
    return datetime.date.fromtimestamp(os.path.getmtime(filename)).isoformat()


def _get_date(filename):
    '''Returns the modification time of `filename` as YYYY-MM-DD.
    
    If PIL is installed, and `filename` refers to a JPG file,
    try to figure out when the picture was taken.
    If the EXIF info is not avaiable, return the file
    modification time.
    '''
    if filename.upper().endswith('.JPG') and _using_exif:
        date = _get_exif_date(filename) or _get_modification_date(filename)
    else:
        date = _get_modification_date(filename)
    return date


def organizedir(path, force=False, dry_run=False):
    '''Organize files from `path` according to their dates.
    
    Set `force` to True to reorganize a directory, even when it seems to be organized.
    Set `dry_run` to True to avoid changes to the file system.
    '''
    if not os.path.isdir(path):
        print "'%s' is not a directory!" % path
        return
    
    organized_path = re.compile(r"^\d{4}-\d{2}-\d{2}")
    
    print "Organizing photos from '%s'" % path
    if dry_run:
        print "Dry run, nothing will be moved, created nor changed."
    
    date_dirnames = {}
    
    basedir = os.path.basename(path) or os.path.basename(os.path.dirname(path))
    if organized_path.match(basedir) and not force:
        print "Skipping '%s'" % basedir
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for name in filenames:
                old = os.path.join(dirpath, name)
                date = _get_date(old)
                date_dirname = "%s ()" % date
                date_dirnames[date_dirname] = date_dirnames.get(date_dirname, 0) + 1
                new = os.path.join(path, date_dirname, name)
                if not dry_run:
                    print "'%s' -> '%s'" % (old, new)
                    os.renames(old, new)
            for name in dirnames[:]:
                if organized_path.match(name):
                    print "Skipping '%s'" % name
                    dirnames.remove(name)
    print
    print "Summary"
    if date_dirnames:
        for dirname in sorted(date_dirnames):
            print "%s: %d files" % (dirname, date_dirnames[dirname])
    else:
        print "Nothing to be organized."


if __name__ == '__main__':
    path = sys.argv[1]
    organizedir(path, dry_run=True)
