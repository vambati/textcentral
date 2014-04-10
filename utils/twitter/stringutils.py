
# simple tokenizer 
import re
REGEX = re.compile(r",\s*")

# TODO: Drop @USER , keep smilies etc
def normalize_twitter(text):
	return text

def normalize(text):
	# String processing 
	out = text.decode('unicode_escape').encode('ascii','ignore')
	#out = text.encode('utf-8')
	out = out.rstrip().lower()
	
	# Cleanup Punctuation 
	
	return out

def tokenize(text):
	return [tok.strip().lower() for tok in REGEX.split(text)]