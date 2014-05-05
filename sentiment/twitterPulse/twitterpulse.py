import sys
import json
import string
import time
import calendar
import datetime
import oauth2 as oauth
import urllib2 as urllib
import matplotlib.pyplot as plt
 

def parseSentiment(file):
    scores = {}
    
    for line in file:
        term, score = line.split("\t")
        scores[term] = int(score)

    return scores


def scoreStream(term):
    moodScores = parseSentiment(open("AFINN-111.txt"))

  
    startTime = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    fig = plt.figure()
    plt.axis([startTime-500, startTime+100, -15, 15])
    plt.title('x')
    fig.canvas.set_window_title('y')
    plt.xlabel('Time')
    plt.ylabel('Sentiment')
    plt.ion()
    plt.show()

    x = [startTime]
    y = [0]
    it = 0

    minAveX = [startTime]
    minAveY = [0]
    minAve = 0
    maCount = 0
    testTime = startTime
	
    f = open(sys.argv[1])
    for line in f:
        n = json.loads(line)

        if "text" in n:
            tw = n["text"].encode('utf-8')
            twStripped = tw.translate(string.maketrans("",""), string.punctuation)
            
            if "retweeted" in n:
                rt = int(n["retweeted"])
            else:
                rt = 0
                
            if "favorite_count" in n:
                fv = int(n["favorite_count"])
            else:
                fv = 0
                    
            oneGrams = tw.split(" ")
        
            score = 0.0
            numGood = 0.0
            numBad = 0.0

            for og in oneGrams:
                if og in moodScores:
                    if moodScores[og] > 0:
                      numGood += 1.0
                    elif moodScores[og] < 0:
                      numBad += 1.0

                    score += float(moodScores[og])

            #score += numGood - numBad + rt + 0.5*fv
            score += numGood - numBad
            
            tTime = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
            x.append(tTime)
            it += 1
            y.append(score)

            maCount += 1
            minAve += score

            if tTime - testTime > 60:
              minAveX.append(tTime)
              minAveY.append(float(minAve)/float(maCount))
              maCount = 0
              minAve = 0
              testTime = tTime

            plt.axis([tTime-300, tTime+60, -15, 15])
            plt.plot(x, y, linewidth=1, color='b')
            plt.plot(minAveX, minAveY, linewidth=2, color='r')

            plt.draw()

            if not score == 0:
              plt.scatter(it, score)
              print tw + "\n  Score = " + str(score) 
              print " "

def main():
    # simple sentiment relations for common words
    sentimentFile = open("AFINN-111.txt")

    searchTerm = []
    # Term to search for in Twitter streams
    
    sysArgs = iter(sys.argv)
    next(sysArgs)

    for a in sysArgs:
      print a
      searchTerm.append(a)
	  
	# Score all tweets 
    scoreStream(searchTerm)

        
if __name__ == '__main__':
    main()
