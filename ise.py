#coding=utf-8
import os
from apiclient.discovery import build
from NLPCore import NLPCoreClient
import sys
import urllib2
import bs4
from bs4 import BeautifulSoup
import re
import operator
from operator import itemgetter
from collections import defaultdict

def sendQuery(service, q):
        res = service.cse().list(
                q=q,
                cx='007382945159574133954:avqdfgjg420',
                ).execute()
        return res

#path to corenlp, pipeline properties, set up search api
dir_path = os.path.dirname(os.path.realpath(__file__))
nlp_path = os.path.join(dir_path, "stanford-corenlp-full-2017-06-09")
client = NLPCoreClient(nlp_path)

p1props = {
        "annotators": "tokenize,ssplit,pos,lemma,ner",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
        }
p2props = {
        "annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation", 
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz", 
        "ner.useSUTime": "0"
        }

service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")
entdict = {1: ["PERSON", "LOCATION"], 2: ["LOCATION", "LOCATION"], 3: ["LOCATION", "ORGANIZATION"], 4: ["PERSON", "ORGANIZATION"]}
reldict = {1: "Live_In", 2: "Located_In", 3: "OrgBased_In", 4: "Work_For"}
# r = sys.argv[1]
# threshold = sys.argv[2]
# q = sys.argv[3]
# k = sys.argv[4]
r = 4
setRelation = reldict[r]
threshold = .35
q = "bill gates microsoft"
k = 10

print("running, wait a long while")
print("iteration 1")
res = sendQuery(service, q)
itercount = 0
seenURLS = []
relationList = []
while len(relationList) < k:
        urls = []
        for page in res['items']:
                url = page['link']
                if url not in seenURLS and "..." not in url:
                        urls.append(url)
                        urls.append(seenURLS)
        
        tempRelList = []
        sentList = []
        #urls = ['https://www.biography.com/people/bill-gates-9307520']
        for pg in urls:
                if type(pg) != list:
                        page = urllib2.urlopen(pg)
                        soup = bs4.BeautifulSoup(page, 'html.parser')
                        page.close()
                        plaintext = ""
                        for stuff in soup.find_all('p'):
                                plaintext = plaintext + " " + stuff.get_text()
                        plaintext = plaintext.encode("utf-8")

                        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', plaintext)
                        # counter = 0
                        # for s in sentences:
                        #         if len(s) < 20 or len(s) > 230:
                        #                 del sentences[counter]
                        #         counter += 1


                        '''PIPELINE 1 '''
                        doc = client.annotate(text=sentences, properties=p1props)
                        #print(doc.sentences[0].tokens[0].ner)
                        #print(doc.sentences[0].tree_as_string())
                        #print(doc.tree_as_string())
                        entities = entdict[r]
                        p2sents = []
                        newsentence = ""
                        for sentence in doc.sentences:
                                #copy entities, remove as found in sentence
                                matchedEntities = list(entities)
                                for token in sentence.tokens:
                                        if token.ner in matchedEntities:
                                                matchedEntities.remove(token.ner)
                                #if all entities removed, its a match!
                                if len(matchedEntities) == 0:
                                        for x in sentence.tokens:
                                                newsentence += " " + x.word
                                        p2sents.append(newsentence.encode("utf-8"))
                                        newsentence = ""

                        print "done with pipeline1"

                ''' PIPELINE 2 '''
                doc = client.annotate(text=p2sents, properties=p2props)
                #print(doc.sentences[0].relations[0])
                for sentence in doc.sentences:
                        for relation in sentence.relations:
                                #check to see if correct relation
                                currentRelation = max(relation.probabilities.iteritems(), key=operator.itemgetter(1))[0]
                                if(currentRelation == setRelation):
                                        #print(type(max(relations.probabilities.iteritems(), key=operator.itemgetter(1))[1]))
                                        currentProb = max(relation.probabilities.iteritems(), key=operator.itemgetter(1))[1]
                                        #print(float(currentProb) >= float(threshold))
                                        #check to see if prob is above threshold
                                        if(float(currentProb) >= threshold):
                                                temp = []
                                                temp.append(currentProb)
                                                temp.append(relation.entities[0].value)
                                                temp.append(relation.entities[0].type)

                                                temp.append(relation.entities[1].value)
                                                temp.append(relation.entities[1].type)

                                                # print(relation.entities[0].type)
                                                # print(relation.entities[0].value)
                                                relationList.append(temp)
                                                tempRelList.append(temp)
                                                for x in sentence.tokens:
                                                        newsentence += " " + x.word
                                                sentList.append(newsentence.encode("utf-8"))
                                                newsentence = ""
                                                print("Success!")
                print "done with pipeline2"

        print("===================== ALL RELATIONS =====================")
        #print all tuples from this set of urls
        if len(tempRelList) != 0:
                tempRelList = sorted(tempRelList, key=itemgetter(0))
        for i in range(0, len(tempRelList)):
                rList = tempRelList[i]
                print "Sentence: ", sentList[i]
                lineString = ("Relation type: " + setRelation + " | Confidence: " + rList[0] +
                                " | Entity #1: " + rList[1] + " (" + rList[2] + ") " +
                                " | Entity #2: " + rList[3] + " (" + rList[4] + ") ")
                print(lineString)
        
        #set duplicates in tuples list to [], then remove all instances of [] from the list
        D = defaultdict(list)
        for i,item in enumerate(relationList):
                tuprepresentation = item[1]+item[3]
                D[tuprepresentation].append(i)
        #keys are tuples, values are the indices of the tuples in relationList
        D = {k:v for k,v in D.items() if len(v)>1}
        for tup,indices in D.iteritems():
                if relationList[indices[0]][0] > relationList[indices[1]][0]:
                        relationList[indices[1]] = []
                else:
                        relationList[indices[0]] = []
        relationList = [x for x in relationList if x != []]

        if len(relationList) < k:
                if len(relationList) == 0:
                        break   #too many iterations have gone by, we've used up all our tuples
                maxx = 0
                maxr = []
                for i in range(0, len(relationList)):
                        if relationList[i][0] > maxx:
                                maxx = relationList[i][0]
                                maxr = relationList[i]
                querytup = maxr[1] + " " + maxr[3]
                res = sendQuery(service, querytup)

                itercount += 1
                print "iteration ", itercount
