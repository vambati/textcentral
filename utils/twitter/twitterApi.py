from twython import Twython, TwythonError
import json
import random,time
import ConfigParser


def login(conf):
	
	config = ConfigParser.RawConfigParser()
	config.read(conf)
	
	CONSUMER_KEY = config.get('twitter','CONSUMER_KEY')
	CONSUMER_SECRET = config.get('twitter','CONSUMER_SECRET')
	ACCESS_TOKEN = config.get('twitter','ACCESS_TOKEN')
	ACCESS_TOKEN_SECRET = config.get('twitter','ACCESS_TOKEN_SECRET')
	
	twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	
	return twitter

def getUserTimeline(api,user):
	try:
	    user_timeline = api.get_user_timeline(screen_name=user)
	except TwythonError as e:
	    print e

	for tweet in user_timeline:
	    print json.dumps (tweet)

########################
def getSearchResults(api,text='paypal'):

	try:
	    search_results = api.search(q=text, count=3000)
	except TwythonError as e:
	    print e

	for tweet in search_results['statuses']:
	    print json.dumps (tweet)
	    #print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at'])
	    #print tweet['text'].encode('utf-8'), '\n'


###################
# TODO 
# API Limits and workarounds
FRIENDS_MAX = 5000
TOTAL_REQUESTS = 0
STATUSES_MAX = 5000
#############

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
	statuses = None
	while statusFlag:
		for i in range(5):
			try:
				statuses = api.GetUserTimeline(user_id=id,page=page,count=200)
				TOTAL_REQUESTS+=1
				break
			except:
				print " FAILED user " + str(id) + ", retrying"
			time.sleep(4)
		
		if statuses!=None and len(statuses) > 0 and len(statusList) < statusLimit:
			#tempList = [(status.GetId(),status.GetUser().GetScreenName(),status.GetCreatedAt(),status.GetRelativeCreatedAt(), status.GetInReplyToScreenName(), status.GetFavorited(), status.GetText()) for status in statuses]
			tempList = [s for status in statuses]
			statusList.extend(tempList)
			if len(statusList) > statusLimit:
				statusFlag = False
			page+=1
		else:
			statusFlag = False
			

	print "Loaded user %d . total %s" % (id,len(statusList))
	return statusList

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
		
# global : move to a class ?
	
if __name__ == '__main__':
	twitterapi = None
	twitterapi = login('vambati.properties')
	#getUserTimeline(twitterapi,"paypal")
	#getSearchResults(twitterapi,"paypal")
	sarr = getStatuses(twitterapi,"paypal")
	json.dumps(sarr)
	
