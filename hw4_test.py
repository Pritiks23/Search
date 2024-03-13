'''Pritika Vipin section AA This file tests
 functions in the Search and Document class'''
from cse163_utils import assert_equals
# import os
import math
from document import Document
from search_engine import SearchEngine
# from cse163_utils import normalize_token


def test_document_term_frequency(doc: Document,
                                 doc2: Document, doc3: Document) -> None:
    '''Test the document_term_frequency method of Document
   class in Documents.py'''
    # Create a Document object with animal-based text
    # Test term frequency for various terms in the document,
    # cuts off at four decimal places
    assert_equals(doc.term_frequency('run'), 2 / 6)
    assert_equals(doc.term_frequency('wolf'), 1 / 6)
    assert_equals(doc.term_frequency('beat'), 1 / 6)
    # Test word not in the document!
    assert_equals(doc.term_frequency('bat'), 0)


def test_document_get_words(doc: Document,
                            doc2: Document, doc3: Document) -> None:
    '''Test the get_words method of Document class
     in Documents.py'''
    # Tests 3 Document object with some sample content
    # Test getting unique, normalized words in the document
    assert_equals(doc.get_words(),
                  ['run', 'wolf', 'beat', 'those', 'chickens'])
    assert_equals(doc2.get_words(),
                  ['chickens'])
    assert_equals(doc3.get_words(),
                  ['marymoor', 'park', 'welcome', 'to',
                   'our', 'favorite', 'house'])


def test_search(doc: Document,
                doc2: Document, doc3: Document, se: SearchEngine) -> None:
    ''' Test search method of Search class in SearchEngine.py.'''
    # se = SearchEngine('/home/folder1/')
    assert_equals(['/home/folder1/parks.txt'], se.search("house"))
    assert_equals(['/home/folder1/animals.txt'], se.search("wolf"))
    assert_equals(['/home/folder1/animals.txt'], se.search("beat"))


def test_calculate_idf(se: SearchEngine) -> None:
    ''' Test _calculate_idf method of Search class
    in SearchEngine.py.'''
    # se = SearchEngine('/home/folder1/')
    # assert_equals(math.log(3), se.search("house"))
    assert_equals(math.log(3), se._calculate_idf("house"))
    assert_equals(math.log(3), se._calculate_idf("run"))
    assert_equals(math.log(3/2), se._calculate_idf("chickens"))


def main():
    '''Main method'''
    animals_doc = Document('/home/folder1/animals.txt')
    empty_doc = Document('/home/folder1/empty.txt')
    parks_doc = Document('/home/folder1/parks.txt')
    se = SearchEngine('/home/folder1/')
    test_document_term_frequency(animals_doc, empty_doc, parks_doc)
    test_document_get_words(animals_doc, empty_doc, parks_doc)
    test_search(animals_doc, empty_doc, parks_doc, se)
    test_calculate_idf(se)


if __name__ == '__main__':
    main()
