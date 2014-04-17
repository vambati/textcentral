# Social String processing library of functions

import re
import sys
import string

# import stopwords file
import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir,'twitter/')
sys.path.insert(0, filename)

from normalizer import Tokenizer 
import stopwords

# Reg-exes 
REGEX = re.compile(r",\s*")
num_format = re.compile("^[1-9][0-9]*\.?[0-9]*")

# A twitter tokenizer 
tw_tok = Tokenizer(preserve_case=False)

# Keep twitter specific tags and smilies etc  
def normalize_twitter(text):
	text = text.decode('unicode_escape').encode('ascii','ignore')
	# tokenize 
	toks = tw_tok.tokenize(text)
	
	# normalize
	toks = remove_stopwords(toks)
	toks = remove_punc(toks)
	toks = remove_numbers(toks)
	
	return toks 

###############################################################################

# A simple tokenize and normalize function that is generic for non-twitter text 
def simple_normalize(text):
	# String processing 
	out = text.decode('unicode_escape').encode('ascii','ignore')
	#out = text.encode('utf-8')
	out = out.rstrip().lower()
	# Cleanup Punctuation 
	return out

def simple_tokenize(text):
	return [tok.strip().lower() for tok in REGEX.split(text)]
	

###############################################################################

def remove_stopwords(toks):
	# Strip punctuation and stopwords
	filtered_toks = [w for w in toks if not w in stopwords.english_stopwords]
	return filtered_toks 
	
def remove_punc(toks):
	punct = set(string.punctuation)
	filtered_toks = [w for w in toks if not w in punct]
	return filtered_toks
	
def remove_numbers(toks):
	filtered_toks = [w for w in toks if not re.match(num_format,w)]
	return filtered_toks
	
###############################################################################
	
if __name__ == '__main__':
    samples = (
        u"RT @ #happyfuncoding: this is a typical Twitter tweet @test :-)",
        u"HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
        u"It's perhaps noteworthy that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123, 4567 are treated as words despite their whitespace."
        )
    
    for s in samples:
        print "======================================================================"
        print s
        tokenized = normalize_twitter(s)
        print "\n".join(tokenized)