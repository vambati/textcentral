#!/usr/bin/env python
from __future__ import division
import sys

###############
# My imports
from textcentral.utils import stringutils 
from textcentral.spam.spammodel import SpamModel
###############

import operator
import getopt
import numpy as np
import string

# Description:
# A spam filter which trains on given input spam data and filters out every spammy sentence 
# STDIN format: ID 	SENTENCE 

# Machine learning for spam detection
from time import time
from pprint import pprint
import pylab as pl
import numpy as np
import sys
import operator

 
def main(separator='\t' ):
	try:
	    opts, args = getopt.getopt(sys.argv[1:],"h:t:")
	except getopt.GetoptError:
	  	print 'run_mapper.py [-m -w -d]'
	  	exit(2)

	# Receive training and test files to load 
	# TODO: Load pre-trained model 

	# Machine learning spam classifier  
	spam_classifier = None
	
	for o,a in opts:
		if(o=='-t'):
			'''load training data for spam detection'''
			trainfile = a
			spam_classifier = SpamModel(trainfile)
		elif(o=='-s'):
			'''load stop_word file for spam detection'''
		   	stopfile = a
		else:
			assert False, "unhandled option"
 
	# Filter out spam from the stream of data 
	for line in sys.stdin:
		line = line.rstrip()
	  	sarr = line.split()
	  	sen = sarr[1]
		result = spam_classifier.score(sen)
		# suppress spam
		if(result==1):
			print line

if __name__ == "__main__":
    main()
