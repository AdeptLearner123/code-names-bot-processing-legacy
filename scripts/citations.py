import wiki_database
import citations_database
from term_pages import TERM_PAGES

def get_page_citations(title):
    page_id = wiki_database.title_to_id(title)
    citation_ids = citations_database.get_citations(page_id)
    citation_titles = wiki_database.get_titles_set(citation_ids)
    return citation_titles


def get_term_citations(term):
    citations = set()
    for title in TERM_PAGES[term]:
        citations.update(get_page_citations(title))
    return citations