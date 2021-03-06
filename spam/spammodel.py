#!/usr/bin/env python
from __future__ import division

from itertools import groupby
from operator import itemgetter
import sys

###############
# import stopwords file
from textcentral.utils import stringutils 

###############

import operator
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
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer 
from sklearn.feature_selection import SelectKBest, chi2

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
from sklearn import cross_validation

from sklearn.metrics import *
from sklearn.cross_validation import StratifiedKFold
from sklearn import preprocessing 

class SpamModel:
	def __init__(self, trainFile=None):

		# Machine learning variables 
		self.vectorizer = None
		self.trainFile = trainFile
		self.classifier = None
	
		# TODO: Tf-IDF transformation
		#self.transformer = TfidfTransformer()
		
		if(self.trainFile!=None):

			# Setup machine learning  
			# 1. Stochastic gradient descent 
			self.classifier = SGDClassifier(alpha=0.0001, class_weight=None, eta0=0.0,fit_intercept=True,learning_rate='optimal', loss='log', n_iter=5, n_jobs=1,penalty='l2', power_t=0.5, rho=0.85, seed=0, shuffle=False,verbose=0, warm_start=False)

			#self.classifier = SGDClassifier(loss="log", penalty="l2")
			#self.classifier = LogisticRegression(C=1.0, penalty='l2')
			#self.classifier = MultinomialNB()
			#self.classifier = RandomForestClassifier()
			#self.classifier = KNeighborsClassifier()
			#self.classifier = svm.SVC()
			
			# Train the classifier 
			self.trainClassifier()
		
		else:
			print ('Error: Nothing to train')
	
	def read_text_file(self,delim):
		f = open(self.trainFile, "r")
		ylabels = []
		tsvData = []
		for s in f:
			# Cleanup of the string (tokenization , lowercasing etc)
			u = stringutils.clean_utf(s)
			tag,line = u.split(delim)
			line =  stringutils.normalize_twitter(line) 

			label = 0
			if(tag=='Y'):
				label = 1
 		
			ylabels.append(label)
			tsvData.append(line)

		return tsvData,ylabels

	def trainClassifier(self):
		(X_train,y_train) = self.read_text_file("\t")

		self.vectorizer = None
		min_n = 1 
		max_n = 2
 
		# Extract training features 
		print ("Extracting features from the training dataset using a sparse vectorizer")
		tfidf_flag = True
		if tfidf_flag==False:
			self.vectorizer = CountVectorizer(ngram_range=(min_n,max_n))
			X_train = self.vectorizer.fit_transform(X_train)
		else:
			self.vectorizer = TfidfVectorizer(sublinear_tf=True,max_df=0.5,ngram_range=(min_n,max_n))
			X_train = self.vectorizer.fit_transform(X_train)
				
		print "Feature generation: n_samples: %d, n_features: %d" % X_train.shape
	
		# Feature Selection - 10 percent reduction in feature size 
		#SELECT_K_FEATURES=X_train.shape[1] / 5;
		
		#print("Extracting %d best features by a chi-squared test")
		#ch2 = SelectKBest(chi2, SELECT_K_FEATURES)
		#X_train = ch2.fit_transform(X_train, y_train)
		#print "Feature selection: n_samples: %d, n_features: %d" % X_train.shape
	 
		# Arra-ize 
		X_train = X_train.toarray()
		y_train = np.array(y_train)
	
		self.classifier.fit(X_train, y_train)

		# Cross validation
		print "5 fold cross validation scores"
		scores = cross_validation.cross_val_score(self.classifier, X_train, y_train, cv=5)
		print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)) 

		# Print top features 
		feature_names = np.asarray(self.vectorizer.get_feature_names())
		print "Top 25 features for each class:"
		for i in range(0,1):
			top10 = np.argsort(self.classifier.coef_[i])[-100:]
			print i,"\n".join(feature_names[top10]) 


	def score(self,sen):
	 	test = []
		sen = stringutils.clean_utf(sen)
		test.append(sen)
		X_test = self.vectorizer.transform(test)
	 
		# Testing 
		X_test = X_test.toarray()
	
		#print ('Predicting on the test set')
		pred = self.classifier.predict(X_test)
		probas = self.classifier.predict_proba(X_test)
 
 		# Labels (0 - Spam ; 1- Not Spam)
		# Labels (0 - Not Relevant ; 1- Relevant)
		label = 1	
		if (probas[0][0] > probas[0][1]):
			label = 0
  
		#print label,"\t",probas[0][0],"\t",sen
		return label

 
###############################################################################
# Testing 
if __name__ == '__main__':
	
     samples = (
         u"RT @ #happyfuncoding: this is a typical Twitter tweet @test :-)",
         u"HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
         u"It's perhaps http://twitter.com noteworthy @gmail or vambati@gmail.com that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123, 4567 are treated as words despite their whitespace."
         )
     spam_classifier = SpamModel(trainFile=sys.argv[1])
     for s in samples:
         print "======================================================================"
         print s,spam_classifier.score(s)
  
