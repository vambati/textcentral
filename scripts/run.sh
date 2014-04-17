touch prada-output/paypal.ngrams
touch prada-output/paypal.ngrams.nospam

for i in `ls ~guest/attensityfeed_janice/*.txt`
do
echo cat $i 
cat $i | python twitter_mapper.py -t d \
	| sort -k1,1 \
	|  python ngram-lm/ngram_top_reducer.py \
	>> prada-output/paypal.ngrams

cat $i | python twitter_mapper.py -t d | python spam/spam_reducer.py -t spam/twitter-spam.txt \
	| sort -k1,1 \
	|  python ngram-lm/ngram_top_reducer.py \
	>> prada-output/paypal.ngrams.nospam
done