#!/usr/bin/env python
"""A mapper to read twitter json strings from Twitter and unpack and release them with a SPAM indicator."""

import sys
import simplejson as json 
import getopt
import dateutil
import dateutil.parser

from textcentral.utils import stringutils
from textcentral.spam.spammodel import SpamModel

import attensity_reader

def read_input(file):
    for line in file:
		pline = attensity_reader.parse(line)
		
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
		(tid,topic,date,text,sentiment,user,gender,ctry,influence_score,followers) = line
		
		# some processing
		text = stringutils.clean_utf(text)
		proc_text = stringutils.normalize_twitter(text)

		# spam indicator 
		spam_flag = spam_classifier.score(text)

		date = date.split('T')[0]

		# Print output 
		out = tid+"\t"+date+"\t"+topic+"\t"+proc_text+"\t"+sentiment+"\t"+str(spam_flag)+"\t"+user+"\t"+gender+"\t"+ctry+"\t"+influence_score+"\t"+followers
		out = out.encode('utf-8')
		print out

 