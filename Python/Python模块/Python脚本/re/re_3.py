#!/usr/bin/env python
# encoding: UTF-8

import re
import datetime
import os

file = 'outpu_1986.10.26.txt'

gettime= re.search("(?P<Year>\d{4})\.(?P<Month>\d{2})\.(?P<Day>\d{2})",file)
#gettime= re.search("(?P<Year>\d+)\.(?P<Month>\d+)\.(?P<Day>\d+)",file)

year = gettime.group('Year')
month = gettime.group('Month')
day = gettime.group('Day')
someday = datetime.date(int(year),int(month),int(day))

someweek = someday.weekday()+1

newname = re.sub('\.','-',file,count=2)

newfile = re.sub('\.','-' + str(someweek)+'.',newname)
print newfile
print someday
print someweek
