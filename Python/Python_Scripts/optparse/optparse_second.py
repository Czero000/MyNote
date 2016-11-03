#!/usr/bin/env python
# encoding: UTF-8

from optparse import OptionParser
usage = "usage:  %prog [-f <filename>] [-n <abc> ... ]"
parser = OptionParser(usage, version="%prog 1.0")

parser.add_option("-f", "--file", action="store", type="string",dest="filename", help="enter a filename")
parser.add_option("-n", "--number",action="store",metavar='int number',type="int",dest="num")
parser.add_option("-v", action="store_true",dest="verbose")
parser.add_option("-q",action="store_false",dest="verbose")
parser.add_option("-x", action="store", dest ="verbose",default="HA", help="%default")
#  option -f
args = ["-f", "foo.txt"]
(options, args) = parser.parse_args(args)
print options.filename

#  optiion -n
args = ["-n", "22"]
(options, args) = parser.parse_args(args)
print options.num

# option -v
fakeargs = ["-v", "Hello"]
(options, args)= parser.parse_args(fakeargs)
print options.verbose

# option -q
fakeargs = ["-q", "bye"]
(options, args) = parser.parse_args(fakeargs)
print options.verbose

# optin -v
fakeargs = [ '-q', 'bye', '-v', 'hello']
(options, args) = parser.parse_args(fakeargs)
print options.verbose

# option -x
(options, args) = parser.parse_args()
print options.verbose
