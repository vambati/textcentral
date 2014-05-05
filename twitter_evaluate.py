import sys 
import sklearn.metrics as metrics

f = open(sys.argv[1])

human=[]
atten=[]

s = f.readline()

for s in f:
	s = s.lower()
	(topic,asent,spam,rel,hsent,text,handle) = s.split('\t')
	
	if(asent == None):
		pass
		
	human.append(hsent)
	
	if(asent=='mixed'):
		asent = 'neutral'
		
	atten.append(asent)
	
print "Accuracy:"
print metrics.accuracy_score(human,atten)

print "F1 Score:"
print metrics.f1_score(human,atten)

print "Precision Score:"
print metrics.precision_score(human,atten)

print "Recall Score:"
print metrics.recall_score(human,atten)

print "Confusion Matrix:"
print metrics.confusion_matrix(human,atten)

print "Report"
print metrics.classification_report(atten,human)