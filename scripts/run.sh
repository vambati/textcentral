touch ../prada-output/paypal.table
touch ../prada-output/paypal.ngrams
touch ../prada-output/paypal.ngrams.nospam

for i in `ls ~guest/attensityfeed_janice/*.txt`
do
echo cat $i 

#cat $i | python twitter_mapper.py -t spam/twitter-spam.txt >>  ../prada-output/paypal.table

#cat $i | python twitter_agg_mapper.py -t d \
#	| sort -k1,1 \
#	|  python ngram-lm/ngram_top_reducer.py \
#	>> ../prada-output/paypal.ngrams

cat $i | python twitter_agg_mapper.py -t d | python spam/spam_filter.py -t spam/twitter-spam.txt \
	| sort -k1,1 \
	|  python ngram-lm/ngram_top_reducer.py \
	>> ../prada-output/paypal.ngrams.nospam
done
