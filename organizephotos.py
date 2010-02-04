#!/usr/bin/env python
import os
import datetime

from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(fn):                                                   
    i = Image.open(fn)
    info = i._getexif()
    return dict([(TAGS.get(tag, tag), value) for tag, value in info.items()])

def organizedir(path):
    for fn in os.listdir(path):
        old = os.path.join(path, fn)
        if not os.path.isfile(old):
            continue
        if fn.upper().endswith('.JPG'):
            date = get_exif(old).get('DateTime')[:10].replace(':', '-')
        else:
            date = datetime.date.fromtimestamp(os.path.getmtime(old)).isoformat()
        new = os.path.join(path, "%s ()" % date, fn)
        print "%r -> %r" % (old, new)
        os.renames(old, new)

for i in range(8, 11):
    path = '/media/Flanders/~Portugal/101MSDCF/1%02dMSDCF' % i
    organizedir(path)

