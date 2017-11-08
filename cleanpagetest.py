import urllib2
import bs4
from bs4 import BeautifulSoup
import os
from NLPCore import NLPCoreClient

url = "https://en.wikipedia.org/wiki/Bill_Gates"
page = urllib2.urlopen(url)
soup = bs4.BeautifulSoup(page, 'html.parser')
plaintext = soup.get_text()

text = ["Bill Gates works at Microsoft.", "Sergei works at Google."] # In actuality, you will want to input the cleaned webpage for the first pipeline, and a list of candidate sentences for the second.

#path to corenlp
dir_path = os.path.dirname(os.path.realpath(__file__))
nlp_path = os.path.join(dir_path, "stanford-corenlp-full-2017-06-09")
print(type(nlp_path))
client = NLPCoreClient(nlp_path)
properties = {
	"annotators": "tokenize,ssplit,pos,lemma,ner", #Second pipeline; leave out parse,relation for first
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz", #Must be present for the second pipeline!
	"ner.useSUTime": "0"
	}
doc = client.annotate(text=text, properties=properties)
#print(doc.sentences[0].tokens[0].ner)
#print(doc.sentences[0].tree_as_string())
#print(doc.tree_as_string())


'''PIPELINE 1 '''
entities = ["PERSON", "ORGANIZATION"]
pip2sents = []
for sentence in doc.sentences:
	#copy entities, remove as found in sentence
	matchedEntities = list(entities)
	for token in sentence.tokens:
		print("ner: " + token.ner) 
		if token.ner in matchedEntities: 
			matchedEntities.remove(token.ner)
	#if all entities removed, its a match!
	if len(matchedEntities) == 0:
		newsentence = ""
		for x in doc.sentences[0].tokens:
			newsentence += " " + x.word
		print(newsentence)
		pip2sents.append(newsentence)




