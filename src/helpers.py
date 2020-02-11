from nltk import bigrams
import spacy
nlp = spacy.load('en_core_web_sm')

# arr is the list of tokens, n is the length of n-gram
def ngrams(arr, n):
	return [arr[i:i+n] for i in range(len(arr)-n+1)]

def prog_print(i, size, width=20):
	prog = round((i / size) * width)
	print('\r|' + prog * '=' + (width - prog) * ' ' + '|', end='')
	if i == size:
		print('\r|' + width*'=' + '|')

def person_filter(tkn_tweet):
	if not len(tkn_tweet):
		return []
	updated_person_noms = []
	for i in bigrams(tkn_tweet):
		first_name = i[0]
		last_name = i[1]
		name = first_name + ' ' + last_name

		doc = nlp(name)
		person_test = ([(X.text, X.label_) for X in doc.ents])

		if not person_test:
			continue
		if person_test[0][1] == 'PERSON':
			updated_person_noms.append(name)
	return updated_person_noms
