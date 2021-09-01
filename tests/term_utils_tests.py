from utils.title_utils import has_suffix
from utils import term_utils
from utils import wiki_database
from utils.term_pages import TERM_PAGES
from utils.term_source_supplements import SOURCE_SUPPLEMENTS


def test_synonyms():
    for term in term_utils.get_terms():
        print("{0}: {1}".format(term, term_utils.get_synonyms(term)))


def test_term_sources():
    for term in term_utils.get_terms():
        source_titles = term_utils.get_term_sources(term)
        print("{0}: {1}".format(term, source_titles))


def test_disambiguation_titles():
    for term in term_utils.get_terms():
        title = term_utils.get_disambiguation_title(term)
        if title is not None and wiki_database.title_exists(title) == False:
            print("Invalid: {0} {1}".format(term, title))


def get_unprocessed_terms():
    for term in term_utils.get_terms():
        source_titles = term_utils.get_term_sources(term)
        source_titles = list(filter(lambda title:not has_suffix(title), source_titles))
        if len(source_titles) == 0 and term not in SOURCE_SUPPLEMENTS:
            print(term)

"""
def test_term_sources():
    for term in TERM_PAGES:
        source_titles = term_utils.get_term_sources(term)
        expected = set(TERM_PAGES[term])
        expected = wiki_database.get_titles_set(wiki_database.get_redirected_ids(wiki_database.get_ids_set(expected)))
        print("{0}: {1}".format(term, expected.difference(source_titles)))
"""