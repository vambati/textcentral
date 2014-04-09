#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys
import simplejson as json 
import getopt
import dateutil
import dateutil.parser

def read_input(file):
    for line in file:
        # split the line into words
	try:
		# Attensity Json load
		#obj = json.loads(line,"ISO-8859-1");
		obj = json.loads(line,"utf-8");
		if(obj['content_subtype'] == 'twitter'):
			user = obj['authors'][0]['screen_name']
			text = obj['title']
			date = obj['published_at']
			sentiment = obj['sentiment']['value']

			# utf encoding 
			user = user.encode('utf-8')
			text = text.encode('utf-8')
		
			# Sentiment analysis
			sent_text="0\t0\t0"
			if(sentiment=='NEUTRAL'):
				sent_text="0\t0\t1"
			elif(sentiment=='POSITIVE'):
				sent_text="1\t0\t0"
			elif(sentiment=='NEGATIVE'):
				sent_text="0\t1\t0"
			else:
				sent_text="0\t0\t0"

			yield user,date,text
			#yield user,date,sent_text
			#yield user,date,1

	except Exception as e:
		#print "error:",e.value
		pass

separator='\t'
key_separator='::'

# time flag 
flag = None
author_flag = False

if __name__ == "__main__":
	try:
        	opts, args = getopt.getopt(sys.argv[1:],"h:t:")
	except getopt.GetoptError:
      		print 'run_mapper.py [-m -w -d]'
      		exit(2)

	for o,a in opts:
		if(o=='-t'):
			'''aggregate at month level'''
		    	flag = a
		elif(o=='-a'):
			'''help'''
		    	author_flag = True
		else:
			assert False, "unhandled option"

	data = read_input(sys.stdin)
	
	for line in data:
		user = line[0]
		date = line[1]
		text = line[2]

		d1 = dateutil.parser.parse(date)
		d = d1.astimezone(dateutil.tz.tzutc())

		if(flag=="d"):
			print d.year,d.month,d.day,separator,text
		elif(flag=="m"):
			print d.year,d.month,separator,text
		elif(flag=="w"):
			print d.year,separator,text

