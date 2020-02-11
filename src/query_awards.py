import sys
import json
from src import helpers
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer as tokenizer
from string import punctuation

def substringSieve(string_list):
	string_list.sort(key=lambda s: len(s), reverse=True)
	out = []
	for s in string_list:
		if not any([s in o for o in out]):
			out.append(s)
	return out

def expand_awards(short_list):
	# person awards - actor or actress
	person = []
	for i in short_list:
		if 'act' in i:
			person.append(i)
	for i in range(0, len(person)):
		person[i] = person[i].replace('best', 'best performance by an')
		if 'motion' in person[i]:
			person.append(person[i] + ' - comedy or musical')
			person[i] = person[i] + ' - drama'

	for i in range(0, len(person)):
		if 'supporting' in person[i]:
			person[i] = person[i].replace('supporting actor', 'actor in a supporting role')
			person[i] = person[i].replace('supporting actress', 'actress in a supporting role')

	for i in range(0, len(person)):
		if 'supporting' in person[i]:
			if '-' in person[i]:
				person[i] = person[i].split(' -')[0]
	for i in range(0, len(person)):
		if 'tv' in person[i]:
			person.append(person[i] + ' - comedy or musical')
			person[i] = person[i].replace('tv', 'television series - drama')
	for i in range(0, len(person)):
		if 'tv' in person[i]:
			person[i] = person[i].replace('tv', 'television series')

	# film or picture
	film_picture = []
	for i in short_list:
		if 'film' in i:
			film_picture.append(i)
		if 'motion picture' in i:
			if not 'act' in i:
				film_picture.append(i)
		if 'television' in i:
			if not 'act' in i:
				film_picture.append(i)
	for i in range(0, len(film_picture)):
		if 'foreign film' in film_picture[i]:
			film_picture[i] = film_picture[i].replace('foreign film', 'foreign language film')
		if '- drama' in film_picture[i]:
			film_picture.append(film_picture[i].replace('- drama', '- comedy or musical'))
		if '- comedy or musical' in film_picture[i]:
			film_picture.append(film_picture[i].replace('- comedy or musical', '- drama'))
		if 'series' in film_picture[i]:
			if not '- drama' in film_picture[i]:
				film_picture.append(film_picture[i].replace('series', 'series - drama'))
				film_picture[i] = film_picture[i].replace('series', 'series - comedy or musical')
			if not '- comedy' in film_picture[i]:
				film_picture.append(film_picture[i].replace('series', 'series - drama'))
				film_picture[i] = film_picture[i].replace('series', 'series - comedy or musical')

	# random awards
	random = []
	for i in short_list:
		if 'direct' in i:
			random.append(i)
		if 'screenplay' in i:
			random.append(i)
		if 'score' in i:
			random.append(i)
		if 'song' in i:
			random.append(i)
	for n in range(0, len(random)):
		if 'song' in random[n]:
			if not 'original' in random[n]:
				random[n] = random[n].replace('song', 'original song')
		if 'score' in random[n]:
			if not 'original' in random[n]:
				random[n] = random[n].replace('score', 'original score')

	new_awards = list(set(random)) + list(set(film_picture)) + list(set(person))
	return new_awards

def main(year):
	# Import twitter data
	with open('data/gg%s.json' % year, 'r') as f:
		data = json.load(f)
	f.close()

	# Generate a list of all stopwords
	punc = ''.split(punctuation)
	english_stop = stopwords.words('english')
	gg_stop = ['goldenglobes', '#goldenglobes', '#goldenglobe', 'golden', 'globes', 'globe']
	twitter_stop = ['&amp;', 'rt']
	stops = set(english_stop + gg_stop + twitter_stop + punc)

	award_candidates = {}

	for n, tweet in enumerate(set([d['text'] for d in data])):
		# Generate all relevant forms of the tweet
		tkn_tweet = tokenizer().tokenize(tweet)
		lower_tweet = [tkn.lower() for tkn in tkn_tweet]
		clean_tweet = [x for x in lower_tweet]
		for sw in set(clean_tweet).intersection(stops):
			clean_tweet.remove(sw)

		if 'best' in clean_tweet:
			tagged_tweet = nltk.pos_tag(clean_tweet)
			for i in range(2, 8):
				ind = clean_tweet.index('best')

				# If we hit the end of the tweet or the last word in the segment isn't a noun, we don't need to look at it
				if ind + i > len(clean_tweet):
					break
				if 'NN' not in tagged_tweet[ind+i-1]:
					continue

				# Find the segment in the uncut tweet, so we have the stopwords
				front, back = lower_tweet.index('best'), lower_tweet.index(clean_tweet[ind+i-1])

				# Piece it together and add it to the candidates list
				name_tkns = lower_tweet[front:back+1]
				for n in range(len(name_tkns)):
					if not name_tkns[n].isalpha():
						name_tkns = name_tkns[:n]
						break
				name = ' '.join(name_tkns)
				if name in award_candidates:
					award_candidates[name] += 1
				else:
					award_candidates[name] = 1

	# Sort dict by number of appearances
	rankings = [(name, v) for name, v in sorted(award_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()

	return expand_awards(substringSieve([i[0] for i in rankings[:40]]))
