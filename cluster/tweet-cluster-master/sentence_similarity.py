#!/usr/bin/env python

import sys
import re
import math

from nltk.corpus import stopwords
from nltk.stem import porter
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

from textcentral.utils import stringutils 

from decorators import memoized

stops = [stop.lower() for stop in stopwords.words('english')]
stemmer = porter.PorterStemmer()
 
def simple_tokenify(s):
    return set([t.lower() for t in s.split()])

def tokenify(s):
	return stringutils.tokenize_twitter(s)
 

def stemify(s):
    return [stemmer.stem(t) for t in s]

def token_frequency(s, t):
    """
    Returns frequency of token, t, in sentence, s.
    """
    regex = r'\b{0}\b'.format(t)
    return len(re.findall(regex, s))

@memoized
def num_docs_containing_token(t, documents):
    return len([doc for doc in documents if t in doc])

def sentence_similarity(s1, s2, documents=None):
    # Shared vocabulary between s1 and s2
    # shared_vocab = set(stemify(tokenify("\n".join((s1, s2)))))
    shared_vocab = set(s1 + s2)

    # Vocabulary across all documents
    documents = documents or []

    # Tokens
    # s1_tokens = tokenify(s1)
    # s2_tokens = tokenify(s2)

    # Stems
    # s1_stems = stemify(s1_tokens)
    # s2_stems = stemify(s2_tokens)

    # Frequencies
    s1_frequencies = dict([(t, s1.count(t)) for t in s1])
    s2_frequencies = dict([(t, s2.count(t)) for t in s2])

    # 
    # Instead of using frequencies, use TF*IDF instead
    # 
    # From: http://en.wikipedia.org/wiki/Tf-idf#Example
    # Consider a document containing 100 words wherein the word cow appears 3 times. 
    # The term frequency (TF) for cow is then (3 / 100) = 0.03. 
    # Now, assume we have 10 million documents and cow appears in one thousand of these. 
    # Then, the inverse document frequency is calculated as log(10 000 000 / 1 000) = 4. 
    # The tf*idf score is the product of these quantities: 0.03 * 4 = 0.12.
    # 
    s1_tf = [(t, f / float(len(s1))) for t, f in s1_frequencies.items()]
    s2_tf = [(t, f / float(len(s2))) for t, f in s2_frequencies.items()]

    s1_tf_idf = dict([(t, f * (math.log10(float(len(documents)) / num_docs_containing_token(t, documents)))) for t, f in s1_tf])
    s2_tf_idf = dict([(t, f * (math.log10(float(len(documents)) / num_docs_containing_token(t, documents)))) for t, f in s2_tf])

    # Matrix
    m = []
    for tf_idf in (s1_tf_idf, s2_tf_idf):
        r = []
        for t in shared_vocab:
            r.append(tf_idf.get(t, 0))
        m.append(r)

    # The following gives a distance, i.e. values close to 0 are very similar
    similarity = math.sqrt(float(sum([pow(m[0][i] - m[1][i], 2) for i in xrange(len(shared_vocab))])))

    return similarity

def simple_sentence_similarity(s1, s2, documents=None):
    # Tokens
    s1_tokens = tokenify(s1)
    s2_tokens = tokenify(s2)

    # Stems
    s1_stems = stemify(s1_tokens)
    s2_stems = stemify(s2_tokens)

    return float(len(s1_stems & s2_stems)) / float(len(s1_stems | s2_stems))

def main(sentences, simple=False):
    similarity_fn = simple_sentence_similarity if simple else sentence_similarity
    for s1 in sentences:
        for s2 in sentences:
            # if s1 is s2:
            #     continue
            if s1 > s2:
                continue    
            print "'{0}'".format(s1), "'{0}'".format(s2), " > ", similarity_fn(s1, s2, sentences)

if __name__ == "__main__":
    # main(("hello world", "HELLO, WORLDS!", "foo bar", "foo bar baz"))
    main(("#hello @world", "HELLO, WORLDS!", "goodbye world http://www.EXAMPLE.com/"))
