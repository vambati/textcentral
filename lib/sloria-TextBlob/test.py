from text.blob import TextBlob

testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
print testimonial.words
print testimonial.tags
print testimonial.noun_phrases
print testimonial.sentiment

zen = TextBlob("Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex.")
print zen.sentences

for sentence in zen.sentences:
	print sentence
	print(sentence.sentiment)
