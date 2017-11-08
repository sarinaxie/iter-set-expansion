import urllib2
import bs4
from bs4 import BeautifulSoup
import os
from NLPCore import NLPCoreClient
import operator

url = "https://www.google.com"
page = urllib2.urlopen(url)
soup = bs4.BeautifulSoup(page, 'html.parser')
plaintext = soup.get_text()

text = ["Bill Gates works at Microsoft.", "Sergei works at Google."] # In actuality, you will want to input the cleaned webpage for the first pipeline, and a list of candidate sentences for the second.
#text = "BIll Gates works at Microsoft. Sergei works at Google."
#path to corenlp
dir_path = os.path.dirname(os.path.realpath(__file__))
nlp_path = os.path.join(dir_path, "stanford-corenlp-full-2017-06-09")
client = NLPCoreClient(nlp_path)

p1props = {
	"annotators": "tokenize,ssplit,pos,lemma,ner", #Second pipeline; leave out parse,relation for first
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz", #Must be present for the second pipeline!
	"ner.useSUTime": "0"
	}
#print(plaintext)
doc = client.annotate(text=text, properties=p1props)
#print(doc.sentences[0].tokens[0].ner)
#print(doc.sentences[0].tree_as_string())
#print(doc.tree_as_string())


'''PIPELINE 1 '''
entities = ["PERSON", "ORGANIZATION"]
p2sents = []
newsentence = ""
for sentence in doc.sentences:
	#copy entities, remove as found in sentence
	print(sentence)
	matchedEntities = list(entities)
	for token in sentence.tokens:
		print("ner: " + token.ner) 
		if token.ner in matchedEntities: 
			print("Match!:" + token.ner)
			matchedEntities.remove(token.ner)
	#if all entities removed, its a match!
	if len(matchedEntities) == 0:
		for x in sentence.tokens:
			newsentence += " " + x.word
		print(newsentence)
		p2sents.append(newsentence)
		newsentence = ""


p2props = {
	"annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation", #Second pipeline; leave out parse,relation for first
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz", #Must be present for the second pipeline!
	"ner.useSUTime": "0"
	}
doc = client.annotate(text=p2sents, properties=p2props)

''' PIPELINE 2 '''
setRelation = "Work_For" 
threshhold = .1
relationList = []
#print(doc.sentences[0].relations[0])
for sentence in doc.sentences:
	for relation in sentence.relations:
		#check to see if correct relation
		currentRelation = max(relation.probabilities.iteritems(), key=operator.itemgetter(1))[0]
		print(currentRelation)
		if(currentRelation == setRelation):
			#print(type(max(relations.probabilities.iteritems(), key=operator.itemgetter(1))[1]))
			currentProb = max(relation.probabilities.iteritems(), key=operator.itemgetter(1))[1]
			#print(float(currentProb) >= float(threshhold))
			#check to see if prob is above threshhold
			if(float(currentProb) >= threshhold):
				temp = []
				temp.append(currentProb)
				temp.append(relation.entities[0].value)
				temp.append(relation.entities[0].type)
				
				temp.append(relation.entities[1].value)
				temp.append(relation.entities[1].type)
				

				print(relation.entities[0].type)
				print(relation.entities[0].value)
				relationList.append(temp)
				print("Success!")
				
print("===================== ALL RELATIONS =====================")
for rList in relationList:
	lineString = ("Relation type: " + setRelation + "Confidence: " + rList[0] +
			" Entity #1: " + rList[1] + " (" + rList[2] + ") " +
			" Entity #2: " + rList[3] + " (" + rList[4] + ") ")
	print(lineString)
			


