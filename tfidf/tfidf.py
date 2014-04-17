#!/usr/bin/python

####
# Load Create and Dump a TF-IDF Matrix 
####

from time import time
from pprint import pprint
import pylab as pl
import numpy as np
import csv
import sys
import operator

# Text proc 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing 


# timing profile 
#from profilehooks import profile

# simple tokenizer 
import re
REGEX = re.compile(r",\s*")

def tokenize(text):
	return [tok.strip().lower() for tok in REGEX.split(text)]

def normalize(text):
	# String processing 
	out = text.decode('unicode_escape').encode('ascii','ignore')
	#out = text.encode('utf-8')
	out = out.rstrip().lower()
	
	# Cleanup Punctuation 	
	return out
 
	
def read_text_file(inpFile,delim):
	f = open(inpFile, "r")
	ylabels = []
	tsvData = []
	for s in f:
		u = normalize(s)
		tag,line = u.split(delim)

		label = 1
		if(tag=='spam'): 
			label = 0
		
		ylabels.append(label)
		tsvData.append(line)

	return tsvData,ylabels

#@profile
def computeTFIDF(data,labels):
	print ("Extracting features from the training dataset using a sparse vectorizer")

	# Option 1
	#vectorizer = CountVectorizer()
	#vectorizer = CountVectorizer(min_n=1, max_n=2,token_pattern=ur'\b\w+\b')
	#vectorizer.min_n = 1 
	#vectorizer.max_n = 2
	#vectorizer.token_pattern=ur'\b\w+\b'
	
	# TF-IDF transformation
	#transformer = TfidfTransformer()

	# Count only
	#data = vectorizer.fit_transform(data)
	#data = transformer.fit_transform(data)	
	
	# Option 2
	# Tf-IDF vectorizer (Counts + TFIDF together )
	#vectorizer = TfidfVectorizer()
	#matrix = vectorizer.fit_transform(data)
	
	# Get max features 
	vectorizer = TfidfVectorizer(max_features=100,analyzer='word')
	matrix = vectorizer.fit_transform(data)
	top_features = vectorizer.vocabulary_
	print top_features
	
 	print "n_samples: %d, n_features: %d" % matrix.shape
	
	#feature_names = np.asarray(vectorizer.get_feature_names())
	#print feature_names
	
	# Sort and get the top tf-idf values 
	stop_words = np.asarray(vectorizer.get_stop_words())
	print stop_words
	

if __name__ == "__main__":
	print ('Loading data sets ')	
	trainFile = sys.argv[1]
	(data,labels) = read_text_file(trainFile,"\t")
 	computeTFIDF(data,labels)
 