#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
twitterCollector.py

Created by Marcel Caraciolo on 2009-11-26.
e-mail: caraciol (at) gmail.com   twitter: marcelcaraciolo
Copyright (c) 2009 Federal University of Pernambuco. All rights reserved.
"""


'''A library that provides a python interface to the Twitter API to collect data'''

__author__ = 'caraciol@gmail.com'
__version__ = '0.1'



FRIENDS_MAX = 20
TOTAL_REQUESTS = 0
STATUSES_MAX = 100


import random,time


def getFriendsInfo(api,usersList,numberOfFriends=FRIENDS_MAX):
	global TOTAL_REQUESTS
	""" Method to get about information of the user's friends
		Parameters:
			api : The twitter api handler
			usersList:  The user ids list
			numberOfFriends: The number of Friends to get
		Return:
			friends : Returns the friends info.
	"""
	friends = []
	#Shuffle the usersList
	random.shuffle(usersList)
	#Get numberofFriends from the list
	if usersList:
		if type(usersList[0]) == type(1): #Is an id ?
			friends = [api.GetUser(nid) for nid in usersList[0:numberOfFriends]]
			TOTAL_REQUESTS+=numberOfFriends
		else: #Is an object ?
			friends = [user for user in usersList[0:numberOfFriends]]
			TOTAL_REQUESTS+=1
	return friends


def getStatuses(api,id=None,statusLimit = STATUSES_MAX ):
	""" Get the statuses from the user 
	Parameters:
		api: The api connector for python-twitter
		id: the twitter ID
		statusLimit: the number of statuses to fetch
	Return:
		statusList: the list of statuses
	"""
	global TOTAL_REQUESTS
	page = 1
	statusFlag = True
	statusList = []
	screenName = None
	while statusFlag:
		for i in range(5):
			try:
				statuses = api.GetUserTimeline(user_id=id,page=page,count=200)
				TOTAL_REQUESTS+=1
				break
			except:
				print " FAILED user " + str(id) + ", retrying"
			time.sleep(4)
			
		if len(statuses) > 0 and len(statusList) < statusLimit:
			tempList = [(status.GetId(),status.GetUser().GetScreenName(),status.GetCreatedAt(),status.GetRelativeCreatedAt(), status.GetInReplyToScreenName(), status.GetFavorited(), status.GetText()) for status in statuses]
			statusList.extend(tempList)
			if len(statusList) > statusLimit:
				statusFlag = False
			page+=1
		else:
			statusFlag = False
			

	print "Loaded user %d . total %s" % (id,len(statusList))
	return statusList
	
	