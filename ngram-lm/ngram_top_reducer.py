#!/usr/bin/env python
from __future__ import division

from itertools import groupby
from operator import itemgetter
import sys

import itertools
import operator
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *

import numpy as np
from scipy.stats import binom
import string

def read_mapper_output(file, separator='\t'):
    for line in file:
		yield line.rstrip().split(separator, 1)

# Routine 1: ngram generator using NLTK 
def ngram_generator_nltk(text,window_size):
	grams = dict()
	words = nltk.word_tokenize(text)
	if(window_size==1):
		grams = words
	elif(window_size==2):
		grams = nltk.bigrams(words)
	elif(window_size==3):
		grams = nltk.trigrams(words)
	
	# ngram counter
	for ng in grams:
		if(ng in ngram):
			ngram[ng]=ngram[ng]+1				
		else:
			ngram[ng]=1
		
	return ngram

# Routine 2: ngram generator  
def ngram_generator(str,ngram,window_size):
	strarr = str.split()
	for n in range (1,window_size+1):
		for i in range(len(strarr)-n+1):
			ng = " ".join(strarr[i:i+n])
			
			# ngram counter
			if(ng in ngram):
				ngram[ng]=ngram[ng]+1				
			else:
				ngram[ng]=1

	return ngram
													
def main(separator='\t'):
    # input comes from STDIN (standard input)
	data = read_mapper_output(sys.stdin, separator=separator)
	for current_word, group in groupby(data, itemgetter(0)):
		try:
			# Create n-grams and score them 
			for current_word, s in group:
				s = s.strip()
				#ngram_generator(str,window_size=1)
				#ngram_generator(str,window_size=2)
				ngram_generator_nltk(s,window_size=3)

			# Sort them in reverse based on frequency counts 
			sorted_x = sorted(ngram.iteritems(), key=operator.itemgetter(1),reverse=True)
			print current_word,sorted_x[:10]
		except ValueError:
			# count was not a number, so silently discard this item
			pass

ngram = dict() 

if __name__ == "__main__":	
    main()
