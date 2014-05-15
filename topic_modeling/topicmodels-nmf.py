#from __future__ import print_function

from time import time
from sklearn.feature_extraction import text
from sklearn import decomposition
from sklearn import datasets
import csv

from textcentral.utils import stringutils

from textcentral import attensity_reader

n_samples  = 5000
n_features = 5000
n_topics = 10
n_top_words = 10


def runTopicAnalyzer():
	vectorizer = text.CountVectorizer(max_df=0.95, max_features=n_features)
	counts = vectorizer.fit_transform(data[:n_samples])
	tfidf = text.TfidfTransformer().fit_transform(counts)
	print("done in %0.3fs." % (time() - t0))

	# Fit the NMF model
	print("Fitting the NMF model on with n_samples=%d and n_features=%d..."% (n_samples, n_features))
	nmf = decomposition.NMF(n_components=n_topics).fit(tfidf)
	print("done in %0.3fs." % (time() - t0))

	# Inverse the vectorizer vocabulary to be able
	feature_names = vectorizer.get_feature_names()

	top_topics = []
	for topic_idx, topic in enumerate(nmf.components_):
		topic_words = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
		top_topics.append(topic_words)
	    
	#print("Topic #%d: %s \t" % (topic_idx,topic_words) )
	print "\t".join(top_topics)

import sys 
inpFile = sys.argv[1]
t0 = time()
print("Loading dataset and extracting TF-IDF features...")

data = []

# Read from flat file
#reader = csv.reader(open(inpFile,'rb'),delimiter='\t')
#for row in reader:
#	data.append(stringutils.normalize_twitter(row[1]))

# Read from json file 
f = open(inpFile,'rb')
for line in f:
	pline = attensity_reader.parse(line)

	if(pline != None):
		(tid,topic,date,twt,sentiment,user,gender,ctry,influence_score,followers) = pline
		data.append(twt)

runTopicAnalyzer()
