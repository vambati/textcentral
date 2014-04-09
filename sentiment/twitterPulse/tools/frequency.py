import sys
import json
import string

def parseTweets(file):

    tweets = []

    for line in file:
        result = json.loads(line)
    
        if "text" in result:
            dic = result["text"].rstrip().replace("\n", "")
            tweets.append(dic)

    return tweets

def main():
    tweet_file = open(sys.argv[1])
    tweets = parseTweets(tweet_file)
    histogram = {}
    total = 0
    for tweet in tweets:
        oneGrams = tweet.split(" ")
        for og in oneGrams:
            if not og.isspace():
                if og.rstrip() in histogram:
                    histogram[og.rstrip()] += 1.0
                else:
                    histogram[og.rstrip()] = 1.0
                total += 1
    
    for name in histogram:
        sys.stdout.flush()
        soln =  histogram[name]/float(total)

        if name.rstrip().isspace():
            continue
        else:
            sys.stdout.flush()
            sys.stdout.write(name + " ")
            sys.stdout.write(str(soln))
            sys.stdout.write("\n")

if __name__ == '__main__':
    main()
