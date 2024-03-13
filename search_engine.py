'''Pritika Vipin AA search_engine.py is the file representing the
 SearchEngine class as well as a command-line
interface for using the SearchEngine'''
import os
import math
from document import Document
from cse163_utils import normalize_token


class SearchEngine:
    '''The SearchEngine class defined in search_engine.py
    represents a corpus of Document objects and includes methods
     to compute the tf–idf statistic between each
      document and a given query. '''
    def __init__(self, corpus_directory: str) -> None:
        '''initializer that takes a str path to
         a directory and constructs an inverted index.'''
        self._corpus_directory: str = corpus_directory
        self._inverted_index: dict = {}

        # Get a list of all files in the corpus directory
        self._files: list = os.listdir(self._corpus_directory)
        self._num_of_files: int = len(self._files)
        # Create a Document object for each file and
        # constructS the inverted index
        for filen in self._files:
            document = Document(os.path.join(self._corpus_directory, filen))
            # document = Document(file_path)
            words_in_document = document.get_words()

            # Update the inverted index with each term and its
            # corresponding Document object
            # If the term has been encountered before adds the document gets
            # added to the dictionary which includes the other documents that
            # contain that term as value(key is that term!)
            for term in words_in_document:
                if term in self._inverted_index:
                    self._inverted_index[term].append(document)
                else:
                    self._inverted_index[term] = [document]

    def _calculate_idf(self, term: str) -> float:
        '''_calculate_idf that takes a str term and
         returns the inverse document frequency of
         that term. If the term is not in the corpus,
        return 0. idf(t) = ln(total # of docs in
        corpus/num of docs that have term t)'''
        # total_documents = len(self.corpus_directory)
        # documents_with_term = len(documents_containing_term)
        if term in self._inverted_index:
            return math.log(self._num_of_files /
                            len(self._inverted_index[term]))
        else:
            return 0

    def __str__(self) -> str:
        '''__str__ that returns a string representation
         of this SearchEngine in the format "SearchEngine({path},
        size: {num_docs})" where path is the
          path to the directory given in the initializer
           and where num_docs is the total
        number of unique documents in the corpus. '''
        return f"SearchEngine({self._corpus_directory}, " \
            f"size: {(self._num_of_files)})"

    def search(self, query: str) -> list[str]:
        """ search that takes a str query that contains
         one or more terms. The search method returns a
          list of document paths sorted in descending order
           by tf–idf statistic. Normalize the terms before
           processing. If there are no matching documents,
        return an empty list. """
        # Normalize the query and split it into individual terms
        normalized_query = [normalize_token(term) for term in query.split()]
        print(normalized_query)
        # Initialize a dictionary to store tf-idf scores for each document
        tfidf_scores = {}
        # For dealing with single-term queries
        if len(normalized_query) == 1:
            term = normalized_query[0]
            idf = self._calculate_idf(term)
            for document in self._inverted_index.get(term, []):
                tf = document.term_frequency(term)
                tfidf_scores[document.get_path()] = tf * idf

        # For dealing with multi-term queries
        else:
            for term in normalized_query:
                idf = self._calculate_idf(term)
                for document in self._inverted_index.get(term, []):
                    tf = document.term_frequency(term)
                    tfidf_scores[document.get_path()] = + \
                        tfidf_scores.get(document.get_path(), 0) + (tf * idf)
        # print(tfidf_scores)
        if len(tfidf_scores.items()) == 0:
            return []
        else:
            # Sort the documents by tf-idf scores in descending order
            # sorts based on the second elment in each list
            scor_and_path = tfidf_scores.items()
            list_tdif = list(scor_and_path)
            sorted_documents = sorted(list_tdif, key=lambda x: x[1],
                                      reverse=True)
            # print(sorted_documents)
        # Return the list of matching document paths in descending tf-idf order
            final = [document[0] for document in sorted_documents]
            return final
