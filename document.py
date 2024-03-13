''' Pritika Vipin Section AA, document.py is the file representing a single
document in the SearchEngine The Document class represents the data
in a single web page and includes methods to compute term frequency.'''
from cse163_utils import normalize_token


class Document:
    """The Document class represents the data
in a single web page and includes methods to compute term frequency """
    def __init__(self, path_to_doc: str) -> None:
        ''' __init__ that takes a path to a document
         and initializes the document data. '''
        self._path: str = path_to_doc
        #  Stores term frequencies in a dict
        self._term_frequencies: dict = {}
        self._uniques: list = []
        self._content: str = ""
        # Open the file to read whats in it
        with open(path_to_doc, 'r') as file:
            self._content = file.read()

        # Breaks into words(tokens) and normalize each token
        tokens = self._content.split()
        self._normalized_words: list = [normalize_token(token)
                                        for token in tokens]

        # Counts occurrences of each term in the doc
        self._total_words: int = len(self._normalized_words)
        self._term_counts: dict = {}
        # Loops and checks If the term has been encountered,
        # if so increments each time it finds the same
        # term in a document. If first time adds it to the
        # term_count dictionary with a value of 1.
        for term in self._normalized_words:
            if term in self._term_counts:
                self._term_counts[term] += 1
            else:
                self._term_counts[term] = 1
        for term in self._term_counts:
            self._uniques.append(term)
        # Compute term frequency for each term
        for term, count in self._term_counts.items():
            self._term_frequencies[term] = count / self._total_words

    def term_frequency(self, term: str) -> float:
        ''' returns the tf of a given term by looking
        it up in the precomputed dictionary. Also normalizes the term.
         If a term not  in a given document, returns 0 '''
        # Normalize the input term
        normalized_term = normalize_token(term)

        # Looks up  term frequency in the precomputed dictionary
        return self._term_frequencies.get(normalized_term, 0)

    def get_path(self) -> str:
        ''' returns the path of the file that this document represents.'''
        return self._path

    def get_words(self) -> list[str]:
        '''Returns list of unique normalized words in the doc'''
        return list(self._uniques)

    def __str__(self) -> str:
        ''' returns a string representation of this document
         in the format "Document({doc_path}, words: {num_words})"
          where doc_path is the path to the document given in the
           Document initializer and where num_words is the total
            number of words in the document.'''
        return f"Document({self._path}, words: {len(self._normalized_words)})"
