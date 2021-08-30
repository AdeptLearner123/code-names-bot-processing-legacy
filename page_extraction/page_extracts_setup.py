import progressbar
import math
from random import sample

from utils import wiki_database
from utils.title_utils import count_title_words
from utils.term_synonyms import get_synonyms
from page_extraction import page_extracts_database
from utils.term_config import NEIGHBORS_ONLY
from utils import term_utils

PAGES_PER_PAIR = 10

def get_term_links():
    id_to_title = wiki_database.get_all_titles_dict()
    page_scores = dict()
    term_links = dict()

    for term in term_utils.get_terms():
        source_titles = term_utils.get_term_sources(term)
        source_ids = wiki_database.get_ids_set(source_titles)
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


def get_multi_links(page_scores):
    multi_links = set(map(lambda item:item[0], filter(lambda item:item[1] >= 3, page_scores.items())))
    return multi_links


def get_pair_links(term_links):
    print("PAIR LINKS")
    terms = term_utils.get_terms()
    all_pair_links = set()

    pairs = math.comb(len(terms), 2)
    iter = 0
    bar = progressbar.ProgressBar(maxval=pairs, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            term1 = terms[i]
            term2 = terms[j]

            links1 = term_links[term1]
            links2 = term_links[term2]
            links = links1.intersection(links2)
            pair_links = sample(links, min(PAGES_PER_PAIR, len(links)))
            all_pair_links.update(pair_links)
            print("{0} | {1}: {2} {3}".format(term1, term2, len(pair_links), len(links)))

            iter += 1
            bar.update(iter)
    
    bar.finish()
    return all_pair_links


def insert_pages(target_links):
    iter = 0
    bar = progressbar.ProgressBar(maxval=len(target_links), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for title in target_links:
        insert_page(title)
        iter += 1
        bar.update(iter)
    bar.finish()
    page_extracts_database.commit()


def insert_page(title, term_links):
    for term in term_utils.get_terms():
        if term not in NEIGHBORS_ONLY or title in term_links[term]:
            for synonym in get_synonyms(term):
                page_extracts_database.insert_term_page(term, synonym, title)


def job():
    page_scores, term_links = get_term_links()
    multi_links = get_multi_links(page_scores)

    for term in term_links:
        term_links[term] = term_links[term].difference(multi_links)

    pair_links = get_pair_links(term_links)
    target_links = multi_links.union(pair_links)
    print("MULTI LINKS: {0}".format(len(multi_links)))
    print("PAIR LINKS: {0}".format(len(pair_links)))
    print("TOTAL: {0}".format(len(target_links)))

    insert_pages(target_links)