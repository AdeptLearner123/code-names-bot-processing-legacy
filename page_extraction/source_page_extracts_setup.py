from page_extraction import page_extracts_database
from utils import title_utils
from utils.term_pages import TERM_PAGES
from utils import wiki_database
from citations import citations
import progressbar


def get_term_words(term, non_source_title_words):
    target_titles = page_extracts_database.get_term_titles(term)
    term_words = set()
    for target_title in target_titles:
        title_words = set(title_utils.extract_title_words(target_title))
        term_words.update(title_words)

    source_ids = wiki_database.get_ids_set(TERM_PAGES[term])
    source_ids = wiki_database.get_redirected_ids(source_ids)
    outgoing_links = wiki_database.fetch_outgoing_links_set(source_ids)
    term_citations = citations.get_term_citations(term)
    outgoing_titles = wiki_database.get_titles_set(outgoing_links)
    outgoing_titles = outgoing_titles.difference(term_citations)
    for title in outgoing_titles:
        title_words = set(title_utils.extract_title_words(title))
        term_words.update(title_words)

    term_words = term_words.intersection(non_source_title_words)    
    return term_words


def job():
    non_source_titles = page_extracts_database.get_non_source_titles()
    non_source_title_words = set()
    for title in non_source_titles:
        non_source_title_words.update(set(title_utils.extract_title_words(title)))

    bar = progressbar.ProgressBar(maxval=len(TERM_PAGES), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in TERM_PAGES:
        term_words = get_term_words(term, non_source_title_words)

        print("{0}: {1}".format(term, len(term_words)))
        for term_source in TERM_PAGES[term]:
            for word in term_words:
                page_extracts_database.insert_term_page(term, word, term_source, True)
        page_extracts_database.commit()

        i += 1
        bar.update(i)
        #print("{0}: {1}".format(term, term_words))
    bar.finish()