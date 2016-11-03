#!/usr/bin/env python
# encoding: UTF-8

from optparse import OptionParser

def main():
    usage = "Usage: %prog [options] arg"
    parser = OptionParser(usage,version="%prog 1.0")
    parser.add_option("-f", "--file",dest="filename",
                       help="read data from filename")
    parser.add_option("-v", "--verbose",
                       action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                       action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        print "reading %s...." %optons.filename

if __name__ == "__main__":
    main()
