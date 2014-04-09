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

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line


def mainproc(sentences):

	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()

	# change this to read in your data
	words = [token for s in sentences for token  in s.lower().split()]
	# filter stop words 
	filtered_words = [w for w in words if not w in stopwords.words('english')]
	# ngram colloc on filtered words 
	finder = BigramCollocationFinder.from_words(filtered_words)
	
	# only bigrams that appear 3+ times
	return finder.apply_freq_filter(3) 	

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    for current_word, group in groupby(data, itemgetter(0)):
        try:
	    sens = list(group)
	    res = mainproc(sens)
	    print current_word,res
        except ValueError:
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    main()
