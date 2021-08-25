from utils.term_pages import TERM_PAGES
from utils import wiki_database
from utils.title_utils import count_title_words
from utils.term_synonyms import get_synonyms
from page_extraction import page_extracts_database

PAGES_PER_LINK = 50

def get_term_links():
    page_scores = dict()
    term_links = dict()
    id_to_title = wiki_database.get_all_titles_dict()

    for term in TERM_PAGES:
        source_titles = TERM_PAGES[term]
        source_ids = wiki_database.get_ids_set(source_titles)
        source_ids = wiki_database.get_redirected_ids(source_ids)
        incoming = wiki_database.fetch_incoming_links_set(source_ids)
        incoming_titles = filter_single_titles(incoming, id_to_title)
        outgoing = wiki_database.fetch_outgoing_links_set(source_ids)
        outgoing_titles = filter_single_titles(outgoing, id_to_title)

        all_links = incoming_titles.union(outgoing_titles)
        double_links = incoming_titles.intersection(outgoing_titles)
        term_links[term] = all_links
        
        for link in all_links:
            if link not in page_scores:
                page_scores[link] = 1
            else:
                page_scores[link] += 1
        for link in double_links:
            page_scores[link] += 0.5

        print("{0}: {1} {2}".format(term, len(all_links), len(double_links)))
    return page_scores, term_links


def filter_single_titles(page_ids, id_to_title):
    filtered_ids = set(filter(lambda id:id in id_to_title, page_ids))
    titles = set(map(lambda id:id_to_title[id], filtered_ids))
    return set(filter(lambda title: count_title_words(title) == 1, titles))


def get_top_links(titles, page_scores):
    sorted_titles = list(sorted(titles, key=lambda title:page_scores[title], reverse=True))
    if "Bivalvia" in sorted_titles:
        print("Bivalvia: {0}".format(sorted_titles.index("Bivalvia")))
    return sorted_titles[:PAGES_PER_LINK]


def insert_page(title):
    for term in TERM_PAGES:
        for synonym in get_synonyms(term):
            page_extracts_database.insert_term_page(term, synonym, title)


def job():
    page_scores, term_links = get_term_links()
    print("Bivalvia Score: {0}".format(page_scores["Bivalvia"]))
    target_titles = set()
    for term in TERM_PAGES:
        print("Getting top: " + term)
        target_titles.update(get_top_links(term_links[term], page_scores))
    #for title in target_titles:
    #    insert_page(title)
    #print("INSERTING: {0}".format(target_titles))
    #page_extracts_database.commit()