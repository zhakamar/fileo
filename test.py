#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from copy import copy

a = [{'odin': '1', 'size': '-'},
	 {'dva': '2', 'size': '42-44'},
	 {'tri': '3', 'size': '46'},
	 {'chet': '4', 'size': '44-48'}]

b = []

for x in a:
	tmp = re.search('(\d{2})-(\d{2})', x['size'])
	if tmp:
		_from, _to = int(tmp.group(1)), int(tmp.group(2)) + 1
		for y in range(_from, _to):
			if (y % 2 == 0):
				x['size'] = y
				print x
				b.append(copy(x))
	else:
		print x
		b.append(x)


print '-' * 15

for x in b:
	print x