import sys
import simplejson as json

for line in sys.stdin:
	obj = json.loads(line,"ISO-8859-1");
	user = obj['user']['screen_name']
	text = obj['text']
	print user 
