#!/usr/bin/env python 

'''Simple algorithm in order to cluster the twitter data'''
 
"""
Algoritm Steps
1 - Get my user data (only statuses - 100 last) ok 
2 - Get all my friends data (only statuses - 100 last) ok
3 - Build the user profile for me and my friends
4 - Run the Hcluster and print the dendogram
5 - Run the scaleDown and print the 2D Map
"""

TOTAL = 0


import twitterT
from twitterCollector import *
import nltk
import string
import pickle
from math import sqrt
from PIL import Image,ImageDraw


def getHeight(clust):
	#Is this an endpoint ? Then the height is just 1
	if clust.left == None and clust.right == None: return 1
	
	#Otherwise the height is the sum of the heights of each branch
	return getHeight(clust.left) + getHeight(clust.right)

def getDepth(clust):
	#The distance of an endpoint is 0.0
	if clust.left == None and clust.right == None: return 0
	
	#The distance of a branch is the greater of its two sides plus its own distance
	return max(getDepth(clust.left),getDepth(clust.right)) + clust.distance
	
def drawDendogram(clust,labels,jpeg='twitterClusters.jpg'):
	#height and width
	h = getHeight(clust)*20
	w = 1200
	depth = getDepth(clust)
	
	#width is fixed, so scale distances accordingly
	scaling = float(w-150)/depth
	
	#Create a new image with a white background
	img = Image.new("RGB", (w,h) , (255,255,255))
	draw = ImageDraw.Draw(img)

	draw.line((0,h/2,10,h/2),fill=(255,0,0))    
	
	# Draw the first node
	drawNode(draw,clust,10,(h/2),scaling,labels)
	img.save(jpeg,'JPEG')
	

def drawNode(draw,clust,x,y,scaling,labels):
	if clust.id < 0:
		h1 = getHeight(clust.left)*20
		h2 = getHeight(clust.right)*20
		top=y-(h1+h2)/2
		bottom=y+(h1+h2)/2
		# Line length
		ll=clust.distance*scaling
		# Vertical line from this cluster to children    
		draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    

		# Horizontal line to left item
		draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    

		# Horizontal line to right item
		draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        

		# Call the function to draw the left and right nodes    
		drawNode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
		drawNode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
	else:   
		# If this is an endpoint, draw the item label
		draw.text((x+5,y-7),labels[clust.id].encode('utf-8'),(0,0,0))



#Pearson distance index
def pearson(v1,v2):
	v1 = [item[1] for item in v1]
	v2 = [item[1] for item in v2]
	
	#Simple sums
	sum1 = sum(v1)
	sum2 = sum(v2)
	
	#Sums of the squares
	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])
	
	#Sum of the products
	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])
	
	#Calculate r (Pearson score)
	num = pSum - (sum1*sum2/len(v1))
	den = sqrt((sum1Sq-pow(sum1,2)/len(v1)) * (sum2Sq-pow(sum2,2)/len(v1)))
	if den == 0: return 0
	
	return 1.0 - num/ den



class bicluster(object):
	def __init__(self, vec, left=None, right=None, distance = 0.0, id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance


def hcluster(data,distance=pearson):
	distances = {}
	currentClustId = -1

	#Clusters are initially just the users
	clust = [bicluster(data[i].items(),id=i) for i in range(len(data))]

	while len(clust) > 1:
		lowestpair = (0,1)
		closest = distance(clust[0].vec,clust[1].vec)
		#loop through every pair looking for the smallest distance
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				#distances is the cache of distance calculations
				if (clust[i].id,clust[j].id) not in distances:
					distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)

				d = distances[(clust[i].id,clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i,j)

		#calculate the average of the two clusters
		mergevec = [(clust[0].vec[i][0], (clust[lowestpair[0]].vec[i][1] + clust[lowestpair[1]].vec[i][1])/2.0) for i in range(len(clust[0].vec))]

		#Create the new cluster
		newcluster = bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]], distance=closest, id=currentClustId)

		#clusters ids that weren't in the original set are negative
		currentClustId-=1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)

	return clust[0]


def printclust(clust,labels=None,n=0):
	# indent to make a hierarchy layout
	for i in range(n): print ' ',
	if clust.id<0:
		# negative id means that this is branch
		print '-'
	else:
		# positive id means that this is an endpoint
		if labels==None: 
			print clust.id
		else: 
			print labels[clust.id]

	# now print the right and left branches
	if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
	if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)




#Parse the statuses and returns the list of words for each text
def getWords(text):
	return stringutils.twitter_tokenize(text)


# Returns the screenname and dictionary of word counts for an twitter user
def getWordCounts(api,user,statusLimit):
	# Parse the user
	statuses = getStatuses(api,user,statusLimit)
	wc = {}
	
	#Loop over all the entries
	for e in statuses:
		text = e[6]
		#Extract a list of words
		words = getWords(text)
		for word in words:
			wc.setdefault(word,0)
			wc[word]+=1
	
	if len(statuses) > 0:
		return statuses[0][1], wc		
	else:
		return api.GetUser(user).GetScreenName(), wc
		


#Step 01: Getting the Twitter Data

#Get My Twitter ID
 
#Get My Friends IDs (only to 5000 friends)
 
#Get all statuses of the users and dump into a temp file
 
#Step 02: Running the Clustering Algorithm

inputF = open('usersData.pk1','rb')
data = [pickle.load(inputF) for i in range(2)]

wordCounts, apCount = data[0],data[1]

#Select all the useful data
wordlist = []
for word, bc in apCount.items():
	wordlist.append(word)


#Join all together for parse it into the cluster algorithm
socialNetworking = {}

for user,wc in wordCounts.items():
	socialNetworking[user] = {}
	for word in wordlist:
		socialNetworking[user].setdefault(word,0)
		if word in wc:
			socialNetworking[user][word] = wc[word]



items  = socialNetworking.items()
users = [item[0] for item in items]
data =  [item[1] for item in items]

#Step 3: Showing the results

clust  = hcluster(data)
drawDendogram(clust,labels=users)


