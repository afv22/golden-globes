import sys
import re
import json
import nltk
from nltk.tokenize import TweetTokenizer as tokenizer
from nltk.corpus import stopwords
from string import punctuation
sw = set(stopwords.words('english'))
import string
from collections import Counter
from datetime import datetime

def main(year):
	with open('data/gg%s.json' % year, 'r') as f:
		db = json.load(f)
	f.close()

	punc = ''.split(punctuation)
	english_stop = stopwords.words('english')
	gg_stop = ['goldenglobes', '#goldenglobes', '#goldenglobe', 'golden', 'globes', 'globe']
	twitter_stop = ['&amp;', 'rt']
	stops = set(english_stop + gg_stop + twitter_stop + punc)

	best_dressed = []

	for tweet in db:
		text = [w.lower() for w in tokenizer().tokenize(tweet['text']) if
					w.lower() not in stops and
					re.fullmatch(r'''[a-z]+''', w.lower())]
		if all([word in text for word in ['best', 'dressed']]):
			best_dressed.append(list(nltk.bigrams(text)))

	clean_bigrams = []

	#only look at tweets with best & dressed
	word_set = set(['best', 'dressed'])

	for bigram_list in best_dressed:
		for bigram in bigram_list:
			if not set(bigram).intersection(word_set):
				clean_bigrams.append(' '.join(bigram))

	top = Counter(clean_bigrams).most_common(50)

	# make sure top bigrams are proper nouns
	for i in top:
		tagged_name = nltk.pos_tag([word.capitalize() for word in i[0].split()])
		if all([tkn[1] == 'NNP' for tkn in tagged_name]):
			return ' '.join([tkn[0] for tkn in tagged_name])

	return 'Nobody dressed well'
