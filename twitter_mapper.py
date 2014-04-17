#!/usr/bin/env python
"""A mapper to read twitter json strings from attensity."""

import sys
import simplejson as json 
import getopt
import dateutil
import dateutil.parser

from textcentral.utils import stringutils
from textcentral.utils.twitter import json_reader

def read_input(file):
    for line in file:
		pline = json_reader.parse(line)
		
		if(pline!=None):
			yield pline
		else:
			pass

separator='\t'
key_separator='::'

# time flag 
flag = None
author_flag = False

if __name__ == "__main__":
	try:
        	opts, args = getopt.getopt(sys.argv[1:],"h:at:")
	except getopt.GetoptError:
      		print 'run_mapper.py [-m -w -d]'
      		exit(2)

	for o,a in opts:
		if(o=='-t'):
			'''aggregate at month level'''
		    	flag = a
		elif(o=='-a'):
			'''aggregate at author level'''
		    	author_flag = True
		else:
			assert False, "unhandled option"

	data = read_input(sys.stdin)
	
	for line in data:
		# Date is the second element, make sure that is the case ! 
		date = line[2]

		d1 = dateutil.parser.parse(date)
		d = d1.astimezone(dateutil.tz.tzutc())

		final_line = "\t".join(line)
		
		# Output author and tweet 
		if(author_flag is True):
			print "@"+user,separator,text
		# Ouptut tweets per time-frame (day | month | year)
		elif(flag=="d"):
			print "%s-%s-%s" %(d.year,d.month,d.day),separator,final_line
		elif(flag=="m"):
			print "%s-%s" %(d.year,d.month),separator,text
		elif(flag=="y"):
			print "%s" %(d.year),separator,text

