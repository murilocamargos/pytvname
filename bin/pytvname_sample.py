#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from pytvname.process import prc

name = 'Banshee.S03e07.HDTV.x264-KILLERS[ettv]'

# We can use the standard format
print(prc(name))

# Or use another format
format = '{showName} {seasonNum}x{episodeNum} {quality}'
print(prc(name, format))

# We can also use another functions form process
from pytvname.process import normalize, info

print(normalize('banshee hdtv'))
print(info(name))

# The qualities and release team names are stored into a json database
# You can add new team names or new quality names
from pytvname.process import Qualities, Teams
qlt = Qualities()
qlt.add("HDTV").save()

tms = Teams()
tms.add("KILLERS").save()

# Or you can use an user interface for it, so the program can ask the user
# the name to be added.
tms = Teams()
tms.addInterface()