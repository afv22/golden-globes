import os
import sys
import json
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
sw = set(stopwords.words('english'))
from src import helpers

def main(year):
	print('\nSearching for hosts...')

	clean_path = 'data/clean_gg' + year + '.json'
	with open(clean_path, 'r') as f:
		all_tweets = json.load(f)
	f.close()

	host_candidates = {}
	tweets = [tweet.split() for tweet in set([' '.join(tweet['clean']) for tweet in all_tweets])]

	size = len(tweets)
	for n, tweet in enumerate(tweets):
		helpers.prog_print(n, size)

		if not any([hw in tweet for hw in ['host', 'Host', 'hosts', 'Hosts']]):
			continue
	
		#get only proper nouns
		tagged = nltk.pos_tag(tweet)
		bigrams = [tagged[i:i+2] for i in range(len(tagged)-1)]
		for bigram in bigrams:
			if all([tkn[1] == 'NNP' for tkn in bigram]):
				name = ' '.join([tkn[0] for tkn in bigram])
				if name in host_candidates:
					host_candidates[name] += 1
				else:
					host_candidates[name] = 1

	rankings = [[k, v] for k, v in sorted(host_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()

	#get top name(s) from rankings
	hosts = [rankings[0][0]]
	ptr = 1
	cutoff = rankings[0][1] * 0.85
	while ptr < len(rankings) and rankings[ptr][1] > cutoff:
		hosts.append(rankings[ptr][0])
		ptr += 1

	return hosts
