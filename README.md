a) Project 1 Group 13

b) README.md transcript.txt ise.py <NAME OF NLP DIRECTORY HERE

c) python ise.py <r> <t> <q> <k>
(r,t,q,k are the same as in the reference implementation)
<r> is an integer between 1 and 4, indicating the relation to extract: 1 is for Live_In, 2 is for Located_In, 3 is for OrgBased_In, and 4 is for Work_For
<t> is a real number between 0 and 1, indicating the "extraction confidence threshold," which is the minimum extraction confidence that we request for the tuples in the output
<q> is a "seed query," which is a list of words in double quotes corresponding to a plausible tuple for the relation to extract (e.g., "bill gates microsoft" for relation Work_For)
<k> is an integer greater than 0, indicating the number of tuples that we request in the output

d) Organization: 
We have one helper function for getting the results of a google search. The main function is responsible for everything else. Additionally, the entire workflow (besides for initializing certain variables) happens in a while loop in the main function.

Workflow:
-initialize the list of relations
-get the top 10 search results from google for query q
-for each url that we have not seen before, retrieve the webpage, extract the plaintext and split the plaintext into a list of sentences
-send the list of sentences through pipeline1 -> the output is a subset of the input
-for each sentence in the outputted list of sentences, run the sentence through pipeline2 and the relation extractor annotator
-if a relation is predicted with a confidence of at least the threshold and it matches the relation that the user requested, add it to a list of relations
-print the relations found for these 10 search results (duplicates may be printed, this is alright according to https://piazza.com/class/j76k8w3eckj12r?cid=56)
-check if there are duplicate tuples (we count different order as different tuple); if there are, delete the ones with lower confidences
-if k or more unique tuples were found among these 10 search results, end
 if less than k tuples were found among these 10 search results, query google with the tuple in the relation list with the highest confidence and go to step 3

e)
3a - we used urllib2 to retrieve the open the webpage. We skip the page if it will cause a timeout.
3b - we extract the plain text using BeautifulSoup. We only look at the text within <p> </p> headers because we assume that almost all relevant sentences will be within those headers. After checking many websites, we felt that assumption was valid.
3c - we split the plain text into sentences using regex, and we append all the sentences to a list. This list of sentences is passed to pipeline 1. Pipeline 1 creates a new list of sentences consisting of only the input sentences that contain entities matching the entities of the relation type we're looking for. This smaller list of sentences is passed to pipeline 2. For each sentence in the new list of sentences, pipeline 2 annotates the sentence and the relation extractor predicts if there is a relation in the sentence. If the predicted relation is of the type we're looking for, has the highest confidence of all the relation types and has a confidence above the threshold, then the tuples for the relation are added to the list of unique tuples.


f)
Search engine API key: AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs
Engine ID: 007382945159574133954:avqdfgjg420
We hardcoded the API key and engine ID into our program though so you don't need this info.

g)
-Differences between us and the reference implementation:
---We print out all the relations in decreasing order of confidence before we remove the duplicates, which is contrary to the assignment on the course website but was allowed by a TA on piazza. (This is stated in the workflow, just repeating it here so it isn't overlooked)
