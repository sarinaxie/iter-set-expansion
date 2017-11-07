from apiclient.discovery import build
import sys 		#to take command line args
import json
import re
from itertools import permutations
from collections import Counter
import operator

#removes html tags, and special characters. Splits on spaces and tabs
def parseWords(string):
	htmlClnr = re.compile('<.*?>')
	string = re.sub(htmlClnr, '', string)
	string = re.sub("[^a-zA-Z 	]+", "", string)
	return string.split()

#takes in file with stopwords, removes them from list
def removeStopWords(tokenList):
	with open('stopWords.txt') as f:
		stopList = f.read().splitlines()
	return [token for token in tokenList if token not in stopList]

#returns most common if not in query already
def mostCommon(tokenList, queryList):
	uniqueList = [token for token in tokenList if token not in queryList]
	freqs = Counter(uniqueList)
	results = [freqs.most_common(2)[0][0], freqs.most_common(2)[1][0]]
	return results

#reorders query using the lists of titles and snippets
def reorder(q, wordsList):
	wordPairs = permutations(q.split(),2)
	wordsString = ' '.join(wordsList)
	newQ = []
	freqs = {}
	for pair in wordPairs:
		pairString = ' '.join(pair)
		if pairString in wordsString:
			freqs[pair] = wordsString.count(pairString)

	sortedPairs = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
	#add pair if not already in query
	for pair in sortedPairs:
		if pair[0][0] not in newQ and pair[0][1] not in newQ: 
				newQ.append(pair[0][0])
				newQ.append(pair[0][1])
	#add words not found in pair
	for word in q.split():
		if word not in newQ:
			newQ.append(word)
	return ' '.join(newQ)

def sendQuery(service, q):
	res = service.cse().list(
		q=q,
		cx='007382945159574133954:avqdfgjg420',
		).execute()
	return res

def main():
	clientKey = sys.argv[1]
	engineKey = sys.argv[2]
	precision = sys.argv[3]
	q = sys.argv[4]
	print ("Parameters:\nClient key = {}\nEngine key = {}\nPrecision = {}\nQuery = {}"
			.format(clientKey, engineKey, precision, q))
	service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")
	
	goalP = float(precision) * 10
	p = -1
	queryList = []
	queryList.extend(q.split())
	while p < goalP and p != 0:
		res = sendQuery(service, q)
		if 'items' not in res:
			print "no response"
			sys.exit()
		if len(res['items']) < 10:
			print "too few results"
			sys.exit()
		print("Google search results:")
		print("============================================")
		print("new query: " + q)
		titles = []
		snippets = []
		p = 0
		
		for page in res['items']:
			tit = page['htmlTitle']
			snip = page['htmlSnippet']
			url = page['displayLink']
			print("\n" + url)
			print(tit + "\n" + snip + "\n")
			mark = raw_input('relevant, y/n?\n')
			if mark.lower() == 'y':
				titles.extend(removeStopWords(parseWords(tit.lower())))
				snippets.extend(removeStopWords(parseWords(snip.lower())))
				p += 1
		if p == 0:
			print "no results"
			sys.exit()
		newWords = mostCommon(titles + snippets, queryList)
		print("new words: ") 
		print(newWords)
		for word in newWords:
			queryList.append(word)
			q = q + " " + str(word)
		q = reorder(q, titles + snippets)
		print("precision: " + str(float(p)/10))
		print("next loop\n")

	print("desired precision reached, done")

if __name__ == '__main__': main()
