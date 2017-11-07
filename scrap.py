import os 
import urllib2
import codecs
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient
from apiclient.discovery import build
service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")
def sendQuery(service, q):
        res = service.cse().list(
                q=q,
                cx='007382945159574133954:avqdfgjg420',
                ).execute()
        return res
'''
clientKey = sys.argv[1]
engineKey = sys.argv[2]
# r = int repping relation type, t = confidence threshold, q = seed query, k = goal num of tuples
r = sys.argv[3]
t = sys.argv[4]
q = sys.argv[5]
k = sys.argv[6]
'''

dir_path = os.path.dirname(os.path.realpath(__file__))
nlp_path = os.path.join(dir_path, "stanford-corenlp-full-2017-06-09")
print(nlp_path)
client = NLPCoreClient(nlp_path)
#client = NLPCoreClient('/path/to/stanford-corenlp-full-2017-06-09')
props1 = {
        "annotators": "tokenize,ssplit,pos,lemma,ner",
        "ner.useSUTime": "0"
}
props2 = {
        "annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
}
q = "cow"
seenURLS = []
res = sendQuery(service, q)
urls = []
for page in res['items']:
        url = page['formattedUrl']
        if url not in seenURLS:
                urls.append(url)
                urls.append(seenURLS)
page = urls[0]
print page
page = urllib2.urlopen(page)
soup = BeautifulSoup(page, 'html.parser')

plaintext = soup.get_text()
fp=codecs.open('delete.txt', 'w',encoding="utf-8")
fp.write(plaintext)
fp.close()
with open('delete.txt', 'r') as myfile:
	data=myfile.read().replace('\n', '')

#trying to get annotate working, pipeline1
	annotext = client.annotate(text=data, properties=props1)
	print(annotext)

