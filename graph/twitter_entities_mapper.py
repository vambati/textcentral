#!/usr/bin/env python
from __future__ import division

from itertools import groupby
from operator import itemgetter
import sys

import operator
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *

import numpy as np
from scipy.stats import binom
import string

from urlparse import urlparse

# Twitter regular expressions
import re 
MENTION = re.compile('\@[a-zA-Z]+')
URL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
HASHTAG = re.compile('\#[\S]+')

def getHashTags(tweet):
	return HASHTAG.findall(tweet)

def getMentions(tweet):
	return MENTION.findall(tweet)

def getURLs(tweet):
	return URL.findall(tweet)
	#o = urlparse(line)
	#return o.netloc

def read_mapper_output(file, separator='\t'):
    for line in file:
		yield line.rstrip().split(separator, 1)

def printEntities(screen_name,tweets):
	# change this to read in your data
	words = [token for s in tweets for token  in s.lower().split()]
	filtered_words = [w for w in words if not w in stopwords.words('english')]
	
	for t in tweets:
		for x in getMentions(t): 
			print screen_name,"\t",x
	
		for x in getHashTags(t): 
			print screen_name,"\t",x

		for x in getURLs(t): 
			print screen_name,"\t",x
	

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    for screen_name, group in groupby(data, itemgetter(0)):
        try:
			tweets = [ t for screen_name, t in group]
			printEntities(screen_name,tweets)
        except ValueError:
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    main()
