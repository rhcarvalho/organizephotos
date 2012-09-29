#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""organizephotos.py - organize your photos in directories by date

Usage:
$ python organizephotos.py /path/to/your/photos
"""

from collections import defaultdict
from datetime import datetime, timedelta
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
        """Returns a dictionary with all the EXIF info of a given image."""
        i = Image.open(filename)
        info = i._getexif() or dict()
        return dict([(TAGS.get(tag, tag), value) for tag, value in info.items()])
    
    def _get_exif_datetime(filename, offset):
        exif = _get_exif(filename)
        datetime_string = exif.get('DateTime')
        datetime_format = "%Y:%m:%d %H:%M:%S"
        try:
            exif_datetime = datetime.strptime(datetime_string, datetime_format)
            offset = timedelta(hours=offset)
            exif_datetime += offset
        except ValueError:
            exif_datetime = None
        return exif_datetime


def _get_modification_datetime(filename):
    return datetime.fromtimestamp(os.path.getmtime(filename))


def _get_date(filename, offset):
    """Returns the modification time of `filename` as YYYY-MM-DD.
    
    If PIL is installed, and `filename` refers to a JPG file,
    try to figure out when the picture was taken.
    If the EXIF info is not avaiable, return the file
    modification time.
    """
    if filename.upper().endswith('.JPG') and _using_exif:
        file_datetime = _get_exif_datetime(filename, offset) or _get_modification_datetime(filename)
    else:
        file_datetime = _get_modification_datetime(filename)
    return file_datetime.date().isoformat()


def organizedir(path, force=False, dry_run=False, offset=0):
    """Organize files from `path` according to their dates.
    
    Set `force` to True to reorganize a directory, even when it seems to be organized.
    Set `dry_run` to True to avoid changes to the file system.
    """
    if not os.path.isdir(path):
        print u"'%s' is not a directory!" % path
        return
    
    organized_path = re.compile(ur"^\d{4}-\d{2}-\d{2}")
    
    print u"Organizing photos from '%s'" % path
    if dry_run:
        print u"Dry run, nothing will be moved, created nor changed."
    
    directory_counter = defaultdict(int)
    
    basedir = os.path.basename(path) or os.path.basename(os.path.dirname(path))
    if organized_path.match(basedir) and not force:
        print u"Skipping '%s'" % basedir
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for name in filenames:
                old = os.path.join(dirpath, name)
                date = _get_date(old, offset)
                organized_directory_name = "%s ()" % date
                directory_counter[organized_directory_name] += 1
                new = os.path.join(path, organized_directory_name, name)
                if not dry_run:
                    print u"'%s' -> '%s'" % (old, new)
                    os.renames(old, new)
            for name in dirnames[:]:
                if organized_path.match(name) and not force:
                    print (u"Skipping '%s'" % name).encode(sys.stdin.encoding, 'replace')
                    dirnames.remove(name)
    print
    print u"Summary"
    if directory_counter:
        for dirname in sorted(directory_counter):
            print u"%s: %d files" % (dirname, directory_counter[dirname])
    else:
        print u"Nothing to be organized."


if __name__ == '__main__':
    print u"OrganizePhotos"
    force = raw_input(u"Reorganize dated folders? [y/N] ") == "y"
    print u"If you took photos when your camera had wrong clock, you can compensate now."
    offset = raw_input(u"Type a value to add to the EXIF date time [0]: ")
    try:
        offset = int(offset)
    except ValueError:
        offset = 0
    move = raw_input(u"Are you sure you want to move the files? [y/N] ") == "y"
    dry_run = not move
    print
    
    paths = sys.argv[1:]
    for path in paths:
        organizedir(unicode(path), force, dry_run, offset)
