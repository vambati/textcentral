import sys
import json
import string


def parseTweets(file):

    tweets = {}

    for line in file:
        result = json.loads(line)
    
        if "entities" in result:
            dic = result["entities"]["hashtags"]
            
            for tag in dic:
                ht = tag["text"]
                if ht in tweets:
                    tweets[ht] += 1
                else:
                    tweets[ht] = 1

    count = 0

    vals = []
    for key, value in sorted(tweets.iteritems(), key=lambda (k,v): (v,k)):
        vals.append([key, value])

    vals.reverse()

    for x in vals:
        print x[0], x[1]
        count += 1
        if count >= 10:
            break
#    return tweets

def main():
 #   sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[1])
    
#    moodScores = parseSentiment(sent_file)
    #print "Scores read"

    tweets = parseTweets(tweet_file)
    #print "Tweets read"
       
if __name__ == '__main__':
    main()
