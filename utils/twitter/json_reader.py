#!/usr/bin/env python
"""A mapper to read twitter json strings from attensity."""

import sys
import simplejson as json 
import getopt
import dateutil
import dateutil.parser

def parse(line):
	try:
        # Attensity Json load
		#obj = json.loads(line,"ISO-8859-1");
		obj = json.loads(line,"utf-8");
		
        # Stripe - 2741 
		#if(obj['content_subtype'] == 'twitter' and obj['topics']['2741']!=None):
        # GoPayments - 2734 
		#if(obj['content_subtype'] == 'twitter' and obj['topics']['2734']!=None):
        # PayPal - 2881 
		if(obj['content_subtype'] == 'twitter' and obj['topics']['2881']!=None):
        # Square - 3061, 2740 
		#if(obj['content_subtype'] == 'twitter' and ((obj['topics']['3061']!=None) or (obj['topics']['2740']!=None))):
			tid = obj['id']
			user = obj['authors'][0]['screen_name']
			text = obj['title']
			date = obj['published_at']
			sentiment = obj['sentiment']['value']
			
			# utf encoding 
			user = user.encode('utf-8')
			text = text.encode('utf-8')
			text = " ".join(text.split())
		
			# Sentiment analysis
			sent_text='0\t0\t0'
			if(sentiment=='NEUTRAL'):
				sent_text='0\t0\t1'
			elif(sentiment=='POSITIVE'):
				sent_text='1\t0\t0'
			elif(sentiment=='NEGATIVE'):
				sent_text='0\t1\t0'
			
			return tid,user,date,text,sent_text
			#return date,proc_text 
			#yield user,date,1

	except Exception as e:
		#print "error:",e.value
		return None

	
if __name__ == '__main__':
	t = '''{"id":"f069d9b91755c7aa98cdd283a7aea486","uri":"http://twitter.com/Gato_Legendario/status/408506060547162112","content_type":"microblog","content_subtype":"twitter","lang":"en","published_at":"2013-12-05T08:00:09Z","published_at_modified":false,"acquired_at":"2013-12-05T08:00:09Z","title":"@humblesupport case 193453, please I want an answer before I\u0027m forced to file a dispute with Paypal :( I don\u0027t want to.","app_source":"web","original_content_id":"408506060547162112","article_urls":[],"correspondence":{"forward":false,"forward_count":0,"reply":false,"recipients":[{"name":"humblesupport","original_author_id":"600286726"}]},"topics":{"2881":"PayPal General"},"authors":[{"name":"Gato Legendario","screen_name":"Gato_Legendario","image_url":"https://pbs.twimg.com/profile_images/378800000802760877/52d34ba9ed518ce9ae76c8c7b44c0ba3_normal.jpeg","gender":"","original_author_id":"1300330004"}],"entities":[{"display_text":"paypal","phrase":"Paypal","domain_role":"ACCOUNT","offset":93,"length":6,"sentiment":"NEUTRAL","projects":[],"semantic_path":"KE_PACKAGES:FINANCE:PRODUCT:ACCOUNT"},{"display_text":"@humblesupport","phrase":"USER__humblesupport__USER","domain_role":"@USERNAME","offset":0,"length":14,"sentiment":"NEUTRAL","projects":[],"semantic_path":"KE_PACKAGES:SOCIAL_MEDIA:AT_USERNAME:@USERNAME"},{"display_text":"negative icon","phrase":"NEGATIVE_ICON","domain_role":"NEGATIVE_ICON","offset":100,"length":2,"sentiment":"NEUTRAL","projects":[],"semantic_path":"KE_PACKAGES:SOCIAL_MEDIA:NEGATIVE_ICON"}],"sentiment":{"value":"NEGATIVE","intent":[]},"metrics":{"klout":13.78080202032612,"reach":0.0,"followers":2,"following":25,"groups":0,"status_updates":15},"geo_location":{"type":"","geometry":{"type":"point","coordinates":[]},"properties":{"country":"","subdivision":"","city":"","admin_division_level_2":"","geo_source":""}},"categories":[],"publisher":"http://twitter.com/Gato_Legendario","outputType":"REAL_TIME"} ''' 
	p = parse(t)
	print p