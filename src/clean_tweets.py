import sys
import re
import json
import nltk
from nltk.tokenize import TweetTokenizer as tokenizer
from nltk.corpus import stopwords
from string import punctuation
from src.helpers import prog_print
from datetime import datetime

#take out different sets of stopwords
english_stop = set(stopwords.words('english'))
gg_stop = ['best', 'goldenglobes', '#goldenglobes', '#goldenglobe', 'golden', 'globes', 'globe']
twitter_stop = ['&amp;', 'rt']
stops = [english_stop, gg_stop, twitter_stop, punctuation]

def clean_tweet(tkns):
	clean_tokens = []

	for tkn in tkns:
		if not any([tkn.lower() in stop for stop in stops]) and \
				not '//t.co/' in tkn and \
				re.fullmatch(r'''[a-zA-Z0-9-'#@]+''', tkn):
			clean_tokens.append(tkn)

	return clean_tokens

def main(year):
	print('Importing %s tweets...' % year)
	with open('data/gg' + year + '.json', 'r') as f:
		db = json.load(f)
	f.close()

	print('Cleaning tweets...')
	tweets = []
	size = len(db)

	start = datetime.now()
	for n, tweet in enumerate(db):
		prog_print(n, size, 40)
		tweets.append({
			'clean': clean_tweet(tokenizer().tokenize(tweet['text'])),
			'raw': tokenizer().tokenize(tweet['text'])})

	print('Time Elapsed:', (datetime.now() - start).seconds // 60)
	print('Saving cleaned tweets...')
	with open('data/clean_gg' + year + '.json', 'w+') as clean_file:
		json.dump(tweets, clean_file)
	clean_file.close()
