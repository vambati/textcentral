#!/usr/bin/env python
from __future__ import division

from itertools import groupby
from operator import itemgetter
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

# Machine learning for spam detection
from time import time
from pprint import pprint
import pylab as pl
import numpy as np
import sys
import operator

 
 
# Map-reduce data reader
def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line


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

		# input comes from STDIN (standard input)
	data = read_mapper_output(sys.stdin, separator='\t')

	# Classifier 
	for current_word, group in groupby(data, itemgetter(0)):
	   try:
		   sens = list(group)
		   for sen in sens:
			# Mark spam vs. no-spam 
			result = spam_classifier.score(sen)
			print current_word,sen,result
	   except ValueError:
	        pass

if __name__ == "__main__":
    main()
