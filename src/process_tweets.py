import sys
import json
from src.queries import query_winner, query_nominees, query_presenters
from src import helpers, sort_tweets

def main(year, award_tweets):

	print('\nProcessing tweets...')
	sw = ['actor', 'actress', 'tv', 'television', 'series', 'film', 'comedy', 'drama', 'director']
	results = {}

	size = len(award_tweets)
	for n, award in enumerate(award_tweets):

		helpers.prog_print(n, size)

		is_person = any([title in award for title in ['actor', 'actress', 'director', 'screenplay', 'original', 'cecil']])

		tweets = award_tweets[award]
		winner = query_winner.main(tweets, award, sw, is_person)

		if is_person:
			nominees = []
		elif 'cecil' in award:
			nominees = [winner]
		else:
			nominees = query_nominees.main(tweets, award, sw, is_person)

		presenters = query_presenters.main(tweets, nominees, award, sw)

		results[award] = {
			'winner': winner,
			'nominees': nominees,
			'presenters': presenters
		}
	print('\r|' + 20*'=' + '|')

	with open('results/partial_gg%s.json' % year, 'w+') as f:
		json.dump(results, f)
	f.close()
