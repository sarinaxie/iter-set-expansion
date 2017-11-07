a) Project 1 Group 13

b)
README.md
transcript.txt
search.py
stopWords.txt

c)
pip install -U google-api-python-client
python search.py AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs 007382945159574133954:avqdfgjg420 <precision> <query>
The stopWords file must be in the same directory or otherwise accessible to the script

Precision needs to be a float and query needs to be in quotes if it is more than one word.
We use python 2.

d) 
Organization:
We divide the code between a main function and multiple helper functions.
The main function is responsible for the main workflow, handling all user input, and making decisions. 
We use various helper funcitons to assist with the processisng of results.

Workflow:
First we get the top 10 search results from google.
Then we print each result one by one and we collect input from the user on whether it is relevant or not.
The titles and summaries of all the relevant results are added to lists that are then passed to the mostCommon() method.
The mostCommon() method returns the two most frequently appearing words in the titles and summaries (that are not a part of the query already) and those two words are added to the query.
After the new words are added to the query, the query is reordered.
We retrieve the top 10 search results for the new query...and the process repeats until we reach the desired precision.

e)

First we remove stopwords, html tags, and special characters from the titles and summaries of the links that are marked relevant.
Then we find the two most frequently appearing words in the titles and summaries that are not part of the query already and we add them to the query.
After the new words are added to the query, we reorder the query.
We do this in a method where we create a list of all possible pairings of the words in the query and then sort the list by how frequently that pairing occurs in a string that is a concatenation of all the relevant titles and summaries.
We add each word in the most frequent pairings to a new list of query terms.
We add any words that were not part of the most frequent pairings but are part of the query to the new query list.
The method returns the new query so it can be passed to the google api.

ex:
query is 'brin'
new words are 'sergey', 'google'
most frequent pairings are ('sergey', 'brin'), ('brin', 'sergey'), ('google', 'brin'), ('brin', 'google')
We add the words 'sergey', 'brin', 'google' to the new query variable.
We did not overlook any words that were present in the original query so now we return the reordered query.

f)
Search engine API key: AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs
Engine ID: 007382945159574133954:avqdfgjg420


g) Used these resources to learn how to find word frequency
https://programminghistorian.org/lessons/counting-frequencies
http://mcsp.wartburg.edu/zelle/python/ppics1/code/chapter11/wordfreq.py

