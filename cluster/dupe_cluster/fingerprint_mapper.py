# map.py

import sys
import re
import string
from fingerprint import FingerPrint

f = FingerPrint()

for line in sys.stdin:
    label,text = line.split('\t')
    try:
	text = text.decode('ascii', 'replace').replace(u'\ufffd', '_')
        print "%s\t%s" % (f.fingerprint(text),text.strip())
    except:
        pass
