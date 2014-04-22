#!/usr/bin/env python
"""A mapper to read twitter json strings from Twitter and unpack and release them with a SPAM indicator."""

import sys
import simplejson as json 
import getopt
import dateutil
import dateutil.parser

from textcentral.utils import stringutils
from textcentral.spam.spammodel import SpamModel
from textcentral.utils.twitter import json_reader

def read_input(file):
    for line in file:
		pline = json_reader.parse(line)
		
		if(pline!=None):
			yield pline
		else:
			pass

SEP='\t'

# time flag 
trainFile = None
spam_classifier = None

if __name__ == "__main__":
	try:
        	opts, args = getopt.getopt(sys.argv[1:],"h:at:")
	except getopt.GetoptError:
      		print 'run_mapper.py [-m -w -d]'
      		exit(2)

	for o,a in opts:
		if(o=='-t'):
			'''Training data file for spam identification'''
			trainFile = a
			spam_classifier = SpamModel(trainFile)
		else:
			assert False, "unhandled option"

	data = read_input(sys.stdin)
	
	for line in data:
		# Modify json_reader.py to change what is packed here ! 
		(tid,user,date,text,sent_text) = line
		
		# some processing
		text = stringutils.clean_utf(text)
		proc_text = stringutils.normalize_twitter(text)

		# spam indicator 
		spam_flag = spam_classifier.score(text)

		date = date.split('T')[0]

		out = tid+"\t"+date+"\t"+user+"\t"+text+"\t"+str(spam_flag)+"\t"+proc_text
		out = out.encode('utf-8')
		print out

 