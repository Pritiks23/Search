# Search
Learning objective: Implement specialized data types with Python classes for tf-idf information retrieval.

search_engine.py is the file representing the SearchEngine class as well as a command-line interface for using the SearchEngine.
document.py is the file representing a single document in the SearchEngine.
hw4_test.py is the file for you to put your own tests. The Run button executes this program.
server.py and index.html provide a web app for you to run your completed search engine. You do not need to look at or modify these files ever.
cse163_utils.py is a helper file that has code to help you test your code.

A search engine is an algorithm that takes a query and retrieves the most relevant documents for that query. In order to identify the most relevant documents, our search engine will use term frequency–inverse document frequency (tf–idf), a text information statistic for determining the relevance of a term to each document from a corpus consisting of many documents.

The tf–idf statistic consists of two components: term frequency and inverse document frequency. Term frequency computes the number of times that a term appears in a document (such as a single Wikipedia page). If we were to use only the term frequency in determining the relevance of a term to each document, then our search result might not be helpful since most documents contain many common words such as "the" or "a". In order to down-weight these common terms, the document frequency computes the number of times that a term appears across the corpus of all documents. The tf–idf statistic takes a term and a document and returns the term frequency divided by the document frequency.

Document

The Document class defined in document.py represents the data in a single web page and includes methods to compute term frequency. (But not document frequency since that would require access to all of the documents in the corpus.)
Task: Write an initializer __init__ that takes a path to a document and initializes the document data. Assume that the file exists, but that it could be empty. In order to implement term_frequency later, we'll need to precompute the term frequency for each term in the document in the initializer by constructing a dictionary that maps each str term to its float term frequency 
tf
tf in the given document.

tf
(
t
,
d
)
=
count of term 
t
 in 
d
count of words in 
d
tf(t,d)= 
count of words in d
count of term t in d
​	
 

Consider the term frequencies for this short document containing 4 total words.

the cutest cutest dog
'the' appears 1 time out of 4 total words, so the 
tf
tf is 0.25.
'cutest' appears 2 times out of 4 total words, so the 
tf
tf is 0.5.
'dog' appears 1 time out of 4 total words, so the 
tf
tf is 0.25.
When constructing this dictionary, normalize all terms by lowercasing text and ignoring punctuation so that 'corgi', 'CoRgi', and 'corgi!!' are considered the same ('corgi'). We have provided a function called normalize_token in cse163_utils.py that you can import to normalize a single token from a string. For example, the following code cells show how to use the function.

token = 'CoRgi!!'
token = normalize_token(token)
print(token)  # corgi

token = '<div>Hi!</div>'
token = normalize_token(token)
print(token)  # divhidiv


If you're familiar with HTML, you might have noticed that a lot of the files in our provided small_wiki corpus contain HTML code, including tags that look like <div>. Don't worry about handling the html. Sticking with what we provide above for normalization is enough.

Task: Write a method term_frequency that returns the 
tf
tf of a given term by looking it up in the precomputed dictionary. Remember to normalize the term. If a term does not appear in a given document, it should have a 
tf
tf of 0.

Task: Write a method get_path that returns the path of the file that this document represents.

Task: Write a method get_words that returns a list of the unique, normalized words in this document.

Task: Write a method __str__ that returns a string representation of this document in the format "Document({doc_path}, words: {num_words})" where doc_path is the path to the document given in the Document initializer and where num_words is the total number of words in the document.

__str__ is a special "magic method" that will be called if you try to print an instance of your class.

Below is an example of expected behavior. Notice how the doc_path is the same as the one passed in to the initializer.

d = Document("/home/dogs.txt")
print(d)
# should print out
# Document(/home/dogs.txt, words: 4)
Be careful when writing assert_equals tests for __str__. You need to call the str function explicitly, like below. If you don’t, you will get an AssertionError that is really quite unhelpful. Remember we don't ever call our magic methods like x.__str__() directly, instead using the Python syntax those functions implement (in this example str(x)).

doc = Document("/home/dogs.txt")
assert_equals("Document(/home/dogs.txt, words: 4)", str(doc))
Task: Write testing functions in hw4_test.py for each function in the Document class. Each testing function must make at least 3 calls to assert_equals using your own test corpus. No spec examples are given for this assessment, and you should not test on hidden staff files. 

Create new files in your workspace for each additional test case. When specifying file names in your code, use absolute paths such as /home/song.txt.

When testing, you must use decimals that terminate within four places (e.g., 0.0125) or precise mathematical expressions (e.g., math.log(7 / 9)).

Bugs in the Document implementation will really hurt when implementing SearchEngine. Make sure to fully test your Document before moving on.


SearchEngine

The SearchEngine class defined in search_engine.py represents a corpus of Document objects and includes methods to compute the tf–idf statistic between each document and a given query.

Task: Write an initializer that takes a str path to a directory such as /home/corpus/ and constructs an inverted index associating each term in the corpus to the list of documents that contain the term. Assume the string represents a valid directory, and that the directory contains only valid files. Do not recreate any behavior that is already done in the Document class—call the Document.get_words method! Create at most one Document object for each file.

In order to implement search later, it will be necessary to find all documents which contain the given term. The initializer for SearchEngine should precompute the inverted index, a dictionary associating each str term to the list of Document objects that include the term. Consider this demonstration corpus of 3 str documents and the inverted index for the corpus.

doc1 = Document("/home/files/corgis.txt")   # File contents: 'I love corgis'
doc2 = Document("/home/files/puppies.txt")  # File contents: 'I love puppies'
doc3 = Document("/home/files/dogs.txt")     # File contents: 'I love dogs'

inverted_index = {
    'i': [doc1, doc2, doc3],
    'love': [doc1, doc2, doc3],
    'corgis': [doc1],
    'puppies': [doc2],
    'dogs': [doc3]
}


The inverted index will help in implementing the search method below by providing a way to answer the question, "Which documents contain the term, 'corgis'?"

To iterate over all the files in a directory, call os.listdir to list all the file names and join the path with os.path.join. 

PYTHON

12345
import osdirectory = '/home/files/'for filename in os.listdir(directory):    print(os.path.join(directory, filename))



Task: Write a method _calculate_idf that takes a str term and returns the inverse document frequency of that term. If the term is not in the corpus, return 0. Otherwise, if the term is in the corpus, compute the inverse document frequency 
idf
idf as follows.

idf
(
t
)
=
ln
⁡
(
total number of documents in corpus
number of documents containing term 
t
)
idf(t)=ln( 
number of documents containing term t
total number of documents in corpus
​	
 )

Call math.log to compute the natural logarithm ln of a given number.

_calculate_idf is a private method, which should not be called by the client. Because it's defined in the SearchEngine class, you should use it to help you implement the search function. We will expect that you have this private method with the behavior described so that we can test your code.


Task: Write a method __str__ that returns a string representation of this SearchEngine in the format "SearchEngine({path}, size: {num_docs})" where path is the path to the directory given in the initializer and where num_docs is the total number of unique documents in the corpus.

Below are examples of expected behavior. Notice how the path printed out by __str__ is always the same as the one passed into the constructor.

se = SearchEngine("/home/files")
print(se) # SearchEngine(/home/files, size: 3)

se2 = SearchEngine("/home/files/")
print(se2) # SearchEngine(/home/files/, size: 3)
Task: Write a method search that takes a str query that contains one or more terms. The search method returns a list of document paths sorted in descending order by tf–idf statistic. Normalize the terms before processing. If there are no matching documents, return an empty list.

To do this, we'll guide you through a 3-step implementation plan.

Handle single-term queries

Start by implementing the search method for queries that contain only a single term. To generate a ranked list of documents, first collect all the documents that contain the given term. Then, compute the tf–idf statistic for each document.

tfidf
(
t
,
d
)
=
tf
(
t
,
d
)
⋅
idf
(
t
)
tfidf(t,d)=tf(t,d)⋅idf(t)

Store these (Document, float) pairs as a list of tuples. Finally, return the sorted list of document paths in descending order according to the tf–idf statistic.

For this assessment, you do not need to worry about tiebreaker cases where two documents have the same tf–idf. Consequently, your assert_equals tests should not have ties. If you encounter a tiebreaker situation it might be an indicator that your search algorithm is incorrectly computing scores for each document!

Test single-term queries

Write your first assert_equals test for search with a single term in hw4_test.py using your own test corpus.

Handle multi-term queries

Extend the search method to queries that contain multiple terms. The output of a multi-term query are all the documents that match at least one term in the query. The tf–idf statistic for multi-term queries is the sum of the single-term tf–idf statistics.

tfidf
(
‘love corgis’
,
d
)
=
tfidf
(
‘love’
,
d
)
+
tfidf
(
‘corgis’
,
d
)
tfidf(‘love corgis’,d)=tfidf(‘love’,d)+tfidf(‘corgis’,d)

Finding the relevant documents for a multi-word query is a bit more challenging. Instead of looking at a single entry in the dictionary, we must look at all Document objects that contain at least one word in the query.

Test multi-term queries

Write a few more assert_equals tests for the search function with multi-word queries in hw4_test.py, using your own test corpus.

Task: Write testing functions in hw4_test.py for each function in the SearchEngine class. Each testing function should contain at least 3 calls to assert_equals using your own test corpus. No spec examples are given for this assessment, and you should not test on hidden staff files.

When testing, you must use decimals that terminate within four places (e.g., 0.0125) or precise mathematical expressions (e.g., math.log(7 / 9)).

How SearchEngine.search works

Now that we have the foundation for the SearchEngine class, let's walk through a full example of the search process. Say we have a corpus named 'other_files' containing 3 documents with the following contents:

/home/other_files/doc1 — Dogs are the greatest pets. 
/home/other_files/doc2 — Cats seem pretty okay 
/home/other_files/doc3 — I love dogs!
This corpus would have the following inverted index

{
    "dogs": [doc1, doc3],
    "are": [doc1],
    "the": [doc1],
    "greatest": [doc1],
    "pets": [doc1],
    "cats": [doc2],
    "seem": [doc2],
    "pretty": [doc2],
    "okay": [doc2],
    "i": [doc3],
    "love": [doc3],
}


Searching this corpus for the query 'love dogs' returns a list in the order ['/home/other_files/doc3', '/home/other_files/doc1'].

Find all matching documents with at least one query word. doc3 contains the word 'love' while both doc1 and doc3 contain the word 'dogs'. Both doc1 and doc3 contain at least one word in the query.
Compute the tf–idf statistic for each matching document. For each matching document, the tf–idf statistic for a multi-word query 'love dogs' is the sum of the tf–idf statistics for 'love' and 'dogs' individually.
tfidf
(
’love dogs’
,
doc1
)
=
0
+
0.081
=
0.081
tfidf(’love dogs’,doc1)=0+0.081=0.081 since 'love' doesn’t appear in doc1.
tfidf
(
’love dogs’
,
doc3
)
=
0.366
+
0.135
=
0.501
tfidf(’love dogs’,doc3)=0.366+0.135=0.501
Associate each matching document with its tf–idf statistic in a list of tuples to sort by descending tf–idf statistic. Return the matching document paths in descending tf–idf order ['/home/other_files/doc3', '/home/other_files/doc1'].
