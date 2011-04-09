#!/usr/bin/env python

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
    return [destination_matchs[name] for name in source_names]

    
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


if __name__ == '__main__':
    main()

