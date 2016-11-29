#!/usr/bin/env python
# encoding: UTF-8

import re
m = re.search('output_(\d{4})','output_1986.txt')
print m.group()
