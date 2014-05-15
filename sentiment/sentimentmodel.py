#!/usr/bin/env python

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

import collections

# Text proc 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer 
from sklearn.feature_selection import SelectKBest, chi2

import sys 
import sklearn.metrics as metrics

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

##################################################
# Base Class 

class SentimentModel:

	# TODO : Will be extended 
	def scoreSentiment(self,s):
		return -1


	# 2. Training lexicon (TFIDF) approach
	def loadLabeledFile(self,file,delim='\t'):
		f = open(file, "r")
		ylabels = []
		tsvData = []
		for s in f:
			# Cleanup of the string (tokenization , lowercasing etc)
			u = stringutils.clean_utf(s)
			tag = ""
			line = ""
			try:
				tag,line = u.split(delim)
				line =  stringutils.normalize_twitter(line) 
			except Exception as e:
				print e
				pass 
				
			asent = 2
			# Load truth
			if(tag=='mixed' or tag=='neutral'):
		 		asent = 2
			elif(tag=='positive'):
				asent = 1
			elif(tag=='negative'):
				asent = 0
			elif(isinstance(tag,int)):
				asent = tag
 		
			ylabels.append(asent)
			tsvData.append(line)

		return tsvData,ylabels
		
	def evaluateFile(self,evalFile):
		
		data,truth = self.loadLabeledFile(evalFile)
		
 		pred=[]
		
		for s in data:		
			# Load predicted 
			p = self.scoreSentiment(s)
			pred.append(p)
	
	
		print "Accuracy:"
		print metrics.accuracy_score(truth,pred)

		print "F1 Score:"
		print metrics.f1_score(truth,pred)

		print "Precision Score:"
		print metrics.precision_score(truth,pred)

		print "Recall Score:"
		print metrics.recall_score(truth,pred)

		print "Confusion Matrix:"
		print metrics.confusion_matrix(truth,pred)

		print "Report"
		print metrics.classification_report(truth,pred)
		
		
##################################################
# 1. Log Probability Lexicon based approach 		

class LogProbSentimentModel(SentimentModel):
	def __init__(self, lexicon=None):

		# Machine learning variables 
		self.lexicon = lexicon
		
		# Multi-Dimensional dictionary
		# TODO 
		#self.log_probs = collections.defaultdict(list)
		
		self.hlog_probs = {}
		self.slog_probs = {}

		
		if(self.lexicon!=None):
			self.loadProbLexicon()
	
	def scoreSentiment(self,s):

		words = stringutils.tokenize_twitter(s)
		
	    # Get the log-probability of each word under each sentiment
		happy_probs = [self.hlog_probs[word]  for word in words if word in self.hlog_probs]
		sad_probs =   [self.slog_probs[word]  for word in words if word in self.slog_probs]

	    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
		tweet_happy_log_prob = np.sum(happy_probs)
		tweet_sad_log_prob = np.sum(sad_probs)

	    # Calculate the probability of the tweet belonging to each sentiment
		prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
		prob_sad = 1 - prob_happy

		print s,tweet_happy_log_prob,tweet_sad_log_prob 
		if(prob_happy>0.65):
			return 1 # Positive
		if(prob_sad >0.65):
			return 0 # Negative
		else:
			return 2 # Neutral

	
	def loadProbLexicon(self):
	    print "Loading lexicon from ",self.lexicon
	    myfile = open(self.lexicon, 'r')
	    myfile.readline() #Ignore title row

	    for line in myfile:
			tokens = line[:-1].split(',')
			self.hlog_probs[tokens[0]]= float(tokens[1])
			self.slog_probs[tokens[0]]= float(tokens[2])


##################################################
	
class TFIDFSentimentModel(SentimentModel):
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
			#self.classifier = SGDClassifier(alpha=0.0001, class_weight=None, eta0=0.0,fit_intercept=True,learning_rate='optimal', loss='log', n_iter=5, n_jobs=1,penalty='l2', power_t=0.5, rho=0.85, seed=0, shuffle=False,verbose=0, warm_start=False)

			#self.classifier = SGDClassifier(loss="log", penalty="l2")
			#self.classifier = LogisticRegression(C=1.0, penalty='l2')
			self.classifier = MultinomialNB()
			#self.classifier = RandomForestClassifier()
			#self.classifier = KNeighborsClassifier()
			#self.classifier = svm.SVC()
			
			# Train the classifier 
			self.trainClassifier()
		
		else:
			print ('Error: Nothing to train')


	def trainClassifier(self):
		(X_train,y_train) = self.loadLabeledFile(self.trainFile,"\t")

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
		#feature_names = np.asarray(self.vectorizer.get_feature_names())
		#print "Top 25 features for each class:"
		#for i in range(0,2):
		#	top10 = np.argsort(self.classifier.coef_[i])[-50:]
		#	print i,"\n".join(feature_names[top10]) 


	def scoreSentiment(self,sen):
	 	test = []
		sen = stringutils.clean_utf(sen)
		test.append(sen)
		X_test = self.vectorizer.transform(test)
	 
		# Testing 
		X_test = X_test.toarray()
	
		#print ('Predicting on the test set')
		pred = self.classifier.predict(X_test)
		probas = self.classifier.predict_proba(X_test)
 
		#print probas 
		# Labels (0 - Negative; 1- Positive; 2-Neutral)
		label = 1
 			
		if (probas[0][0] > probas[0][1] and probas[0][0] > 0.25):
			label = 0
		elif (probas[0][0] < probas[0][1] and probas[0][1] > 0.25):
			label = 1
		else:
			label = 2
  
		#print label,"\t",probas[0][0],"\t",sen
		return label

###############################################################################

# Testing 
if __name__ == '__main__':
	
     samples = (
         u"RT @ #happyfuncoding: this is a typical Twitter tweet @test i love it :-)",
         u"HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
         u"It's perhaps http://twitter.com noteworthy @gmail or vambati@gmail.com that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123, 4567 are treated as words despite their whitespace."
         )

     #sent_classifier = TFIDFSentimentModel(trainFile=sys.argv[1])
     
     sent_classifier = LogProbSentimentModel(lexicon=sys.argv[1])
	 
     for s in samples:
         print "======================================================================"
         print s,sent_classifier.scoreSentiment(s)
  
  
      # Evaluate on a larger file
     if(len(sys.argv)>2):
        sent_classifier.evaluateFile(sys.argv[2])
	  
