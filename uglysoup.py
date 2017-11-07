import urllib2
import bs4 import BeautifulSoup
from NLPCore import NLPCoreClient

from apiclient.discovery import build

service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")

def sendQuery(service, q):
	res = service.cse().list(
		q=q,
		cx='007382945159574133954:avqdfgjg420',
		).execute()
	return res

clientKey = sys.argv[1]
engineKey = sys.argv[2]
# r = int repping relation type, t = confidence threshold, q = seed query, k = goal num of tuples
r = sys.argv[3]
t = sys.argv[4]
q = sys.argv[5]
k = sys.argv[6]
client = NLPCoreClient('/path/to/stanford-corenlp-full-2017-06-09')
properties = {
	"annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
	"ner.useSUTime": "0"
}

relcount = 0
seenURLS = []
while relcount != k:
	res = sendQuery(service, q)
	
	urls = []
	for page in res['items']:
		url = page['displayLink']
		if url not in seenURLS:
			urls.append(url)
			urls.append(seenURLS)
	for page in urls:
		page = urllib2.open(page)
		soup = BeautifulSoup(page, 'html.parser')
		plaintext = soup.get_text()
		plaintext.annotate(text=, properties=properties)
		print(doc.sentences[0].relations[0])
		
		#hmmmmmmmmm relations
