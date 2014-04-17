#!/usr/bin/env python
from __future__ import division

from itertools import groupby
from operator import itemgetter
import sys

# import stopwords file
import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir,'twitter/')
sys.path.insert(0, filename)

import operator
import nltk
from nltk.collocations import *
import getopt
import numpy as np
from scipy.stats import binom
import string

# Machine learning for spam detection
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

from sklearn import svm
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier, LassoLars,Lasso
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.extmath import density
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import *
from sklearn.cross_validation import StratifiedKFold
from sklearn import preprocessing 


# simple tokenizer 
import re
REGEX = re.compile(r",\s*")

# TODO: Drop @USER , keep smilies etc
def normalize_twitter(text):
	return text

def normalize(text):
	# String processing 
	out = text.decode('unicode_escape').encode('ascii','ignore')
	#out = text.encode('utf-8')
	out = out.rstrip().lower()
	
	# Cleanup Punctuation 
	
	return out

def tokenize(text):
	return [tok.strip().lower() for tok in REGEX.split(text)]
	
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

def trainClassifier(trainFile):

	print ('Loading data sets ')
	(X_train_data,y_train_labels) = read_text_file(trainFile,"\t")

	print ("Extracting features from the training dataset using a sparse vectorizer")
	vectorizer = CountVectorizer()
	#vectorizer = CountVectorizer(min_n=1, max_n=2,token_pattern=ur'\b\w+\b')
	#vectorizer.min_n = 1 
	#vectorizer.max_n = 2
	#vectorizer.token_pattern=ur'\b\w+\b'

	# Extract training features 
	X_train = vectorizer.fit_transform(X_train_data)
	print "n_samples: %d, n_features: %d" % X_train.shape

	# TODO: Tf-IDF transformation
	#transformer = TfidfTransformer()
	#X_train = transformer.fit_transform(X_train)

	# Arra-ize 
	X_train = X_train.toarray()
	y_train = np.array(y_train_labels)
	
	
	# Setup machine learning  
	# 1. Stochastic gradient descent 
	#classifier = SGDClassifier(alpha=0.0001, class_weight=None, eta0=0.0, fit_intercept=True,
	#       learning_rate='optimal', loss='log', n_iter=5, n_jobs=1,
	#       penalty='l2', power_t=0.5, rho=0.85, seed=0, shuffle=False,
	#       verbose=0, warm_start=False)

	#classifier = SGDClassifier(loss="log", penalty="l2")
	#classifier = LogisticRegression(C=1.0, penalty='l1')
	classifier = MultinomialNB()
	#classifier = RandomForestClassifier()
	#classifier = KNeighborsClassifier()
	#classifier = svm.SVC()

	classifier.fit(X_train, y_train)

	# Cross validation
	#classifier.cross_validation()
	print ('Training the model: Done')
 
	return vectorizer,classifier

def scoreClassifier_one(sen,vectorizer,classifier):
 	test = []
	test.append(sen)
	X_test = vectorizer.transform(test)
	#print "n_samples: %d, n_features: %d" % X_test.shape
	 
	# Testing 
	X_test = X_test.toarray()
	
	#print ('Predicting on the test set')
	pred = classifier.predict(X_test)
	probas = classifier.predict_proba(X_test)
 
	label = 1	
	if (probas[0][0] > probas[0][1]): label = 0
  
	#print label,"\t",probas[0][0],"\t",sen
	return label
	
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

	# Machine learning variables 
	trainfile = None
	vectorizer = None
	transformer = None
	myModel = None 
	for o,a in opts:
		if(o=='-t'):
			'''load training data for spam detection'''
		   	trainfile = a
			vectorizer, classifier = trainClassifier(trainfile)
		elif(o=='-s'):
			'''load stop_word file for spam detection'''
		   	stopfile = a
		else:
			assert False, "unhandled option"

		# input comes from STDIN (standard input)
	data = read_mapper_output(sys.stdin, separator='\t')

	for current_word, group in groupby(data, itemgetter(0)):
	   try:
		   sens = list(group)
		   for sen in sens:
			# Mark spam vs. no-spam 
			sen = normalize(sen)
			result = scoreClassifier_one(sen,vectorizer,classifier)
			print current_word,sen,result
	   except ValueError:
	        # count was not a number, so silently discard this item
	        pass

if __name__ == "__main__":
    main()


# TODO: Show metrics when using a test file associated with it 
def metrics():

	# Metrics: 
	# Compute Precision-Recall and plot curve
	prec = precision_score(y_test, y_pred)
	print ("Precision: %f" % prec )
	rec = recall_score(y_test, y_pred)
	print ("Recall: %f" % rec)
	f1 = f1_score(y_test, y_pred)
	print ("F1-score: %f" % f1) 

	acc = zero_one_score(y_test, y_pred)
	print ("Accuracy (0/1): %f" % acc)
	#report = classification_report(y_test, y_pred)
	#print report