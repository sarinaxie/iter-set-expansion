a) Project 1 Group 13

b) README.md transcript.txt ise.py <NAME OF NLP DIRECTORY HERE

c) python <r> <t> <q> <k>
(r,t,q,k are the same as in the reference implementation)
<r> is an integer between 1 and 4, indicating the relation to extract: 1 is for Live_In, 2 is for Located_In, 3 is for OrgBased_In, and 4 is for Work_For
<t> is a real number between 0 and 1, indicating the "extraction confidence threshold," which is the minimum extraction confidence that we request for the tuples in the output
<q> is a "seed query," which is a list of words in double quotes corresponding to a plausible tuple for the relation to extract (e.g., "bill gates microsoft" for relation Work_For)
<k> is an integer greater than 0, indicating the number of tuples that we request in the output

d) Steps:
-get the top 10 search results from google for query q
-for each url that we have not seen before, retrieve the webpage, extract the plaintext and split the plaintext into a list of sentences
-send the list of sentences through pipeline1 -> the output is a subset of the input
-send the outputted list of sentences through pipeline2 and the relation extraction, sentence by sentence
-

e)

f)
Search engine API key: AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs
Engine ID: 007382945159574133954:avqdfgjg420
We hardcoded the API key and engine ID into our program though so you don't need this info.

g)
