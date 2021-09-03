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
        sources = term_utils.get_term_sources(term)
        for source in sources:
            if not wiki_database.title_exists(source):
                print("Title doesn't exist: {0}".format(source))
                continue
            source_id = wiki_database.title_to_id(source)
            if wiki_database.get_redirect(source_id) is not None:
                print("Redirected: {0}->{1}".format(source, wiki_database.get_redirected_title(source)))


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