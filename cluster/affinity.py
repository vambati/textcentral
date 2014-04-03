import numpy as np
import sys
import csv 


from sklearn.cluster import AffinityPropagation
from sklearn import metrics

# Text proc 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import codecs

def read_text_file(inpFile,delim):
	f = open(inpFile, "r")
        ylabels = []
        tsvData = []
	for s in f: 
	  try:
		u = s.encode('utf-8')
		label,line = u.split(delim)
                ylabels.append(label)
                tsvData.append(line)
	  except:
		pass

        return tsvData,ylabels


##############################################################################
# Generate sample data
X,labels = read_text_file(sys.argv[1],"\t")
vectorizer = CountVectorizer()
transformer = TfidfTransformer()
X = vectorizer.fit_transform(X)

# Arra-ize 
X = X.toarray()
#y = np.array(labels)

print "Affinity Clustering..."
print X

##############################################################################
# Compute Affinity Propagation
af = AffinityPropagation().fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))


##############################################################################
# Plot result
import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    pl.plot(X[class_members, 0], X[class_members, 1], col + '.')
    pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()


