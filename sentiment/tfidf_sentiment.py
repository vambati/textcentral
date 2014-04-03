#!/usr/bin/python

####
# Vamshi - 16 June 2012 
# Trying out the algorithms for sentiment analysis 
#####

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


# timing profile 
#from profilehooks import profile

# simple tokenizer 
import re
REGEX = re.compile(r",\s*")

def tokenize(text):
	return [tok.strip().lower() for tok in REGEX.split(text)]

def read_text_file(inpFile,delim):
	reader = csv.reader(open(inpFile,'rb'),delimiter=delim)

	# Gold standard labels (first column) 
	ylabels = []
	# Training data (features) 
	tsvData = []

	#Iterate through the file 
	for row in reader:
		ylabels.append(row[0])
		tsvData.append(row[1])

	return tsvData,ylabels

def train_test(X_train, y_train, X_test, y_test):

	# Training 
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

	print ('Training the model ')
	myModel = classifier.fit(X_train, y_train)

	# Cross validation
	#myModel.cross_validation()

	# Testing 
	print ('Predicting on the test set')
	y_pred = myModel.predict(X_test)
	y_probas = classifier.predict_proba(X_test)
	print (y_probas)

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
	 
	print ("Confusion Matrix(0/1): ") 
	#confusionmatrix = confusion_matrix(y_test,y_pred)
	#print confusionmatrix

	#precision, recall, thresholds = precision_recall_curve(y_train, probas_)
	#area = auc(recall, precision)
	#print "Area Under Curve: %0.2f" % area
	return y_probas

#@profile
def main():
	trainFile = sys.argv[1]
	testFile = sys.argv[2]
	print ('Loading data sets ')
	(X_train_data,y_train_labels) = read_text_file(trainFile,"\t")
	print ("Loaded training data ")

	print ("Extracting features from the training dataset using a sparse vectorizer")
	vectorizer = CountVectorizer()
	#vectorizer = CountVectorizer(min_n=1, max_n=2,token_pattern=ur'\b\w+\b')
	#vectorizer.min_n = 1 
	#vectorizer.max_n = 2
	#vectorizer.token_pattern=ur'\b\w+\b'

	# Tf-IDF transformation
	transformer = TfidfTransformer()

	# Extract training features 
	X_train = vectorizer.fit_transform(X_train_data)
	#print "n_samples: %d, n_features: %d" % X_train.shape
	#X_train = transformer.fit_transform(X_train)

	# Load testing data with the same vectorizer 
	(X_test_data,y_test_labels)  = read_text_file(testFile,"\t")

	X_test = vectorizer.transform(X_test_data)
	#print "n_samples: %d, n_features: %d" % X_test.shape
	#X_test = transformer.transform(X_test)

	# Arra-ize 
	X_train = X_train.toarray()
	y_train = np.array(y_train_labels)

	X_test = X_test.toarray()
	y_test = np.array(y_test_labels)
	print ("Loaded test data ")

	probas = train_test( X_train, y_train, X_test, y_test)

	i = 0
	for x in X_test_data:
		if (probas[i][0] > probas[i][1]): label = 0
		else: label = 1
		print label,"\t",probas[i][0],"\t",probas[i][1]
		i=i+1

if __name__ == "__main__":
	main()

#if opts.select_chi2:
#    print ("Extracting %d best features by a chi-squared test" %
#           opts.select_chi2)
#    t0 = time()
#    ch2 = SelectKBest(chi2, k=opts.select_chi2)
#    X_train = ch2.fit_transform(X_train, y_train)
#    X_test = ch2.transform(X_test)
#    print "done in %fs" % (time() - t0)


