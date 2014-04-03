import sys
import json
import string


def parseSentiment(file):
    scores = {}
    
    for line in file:
        term, score = line.split("\t")
        term = term.rstrip()
        scores[term] = int(score)

    return scores

def parseTweets(file):

    tweets = []

    for line in file:
        result = json.loads(line)
    
        if "text" in result:
            dic = result["text"].rstrip().replace("\n","")
            tweets.append(dic)

    return tweets

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", "each", "few", "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "lets", "me", "more", "most", "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shant", "she", "shed", "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "were", "werent", "what", "whats", "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"]

    moodScores = parseSentiment(sent_file)
    #print "Scores read"

    tweets = parseTweets(tweet_file)
    #print "Tweets read"

    newWords = {}

    for tweet in tweets:
        oneGrams = tweet.split(" ")
        
        score = 0

        tempNewWords = []

        for og in oneGrams:
            if og.rstrip() in moodScores:
                score += int(moodScores[og.rstrip()])
            elif og not in tempNewWords:
                tempNewWords.append(og.rstrip())

        for n in tempNewWords:
                if n in newWords:
                    newWords[n][0] += score
                    newWords[n][1] += 1
                else:
                    newWords[n] = [score, 1]

    for x in newWords:
        sys.stdout.flush()
        soln =  float(newWords[x][0])/float(newWords[x][1])

        if x.rstrip().isspace():
            continue
        elif x:
            sys.stdout.flush()
            print x.encode('utf-8', 'ignore'),
            sys.stdout.write(" " + str(soln))
            sys.stdout.write("\n")
        
if __name__ == '__main__':
    main()
