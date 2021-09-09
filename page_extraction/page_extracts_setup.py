from tqdm import tqdm
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
        source_ids = term_utils.get_source_ids(term)
        incoming = wiki_database.fetch_incoming_links_set(source_ids)
        incoming = filter_single_titles(incoming, id_to_title)
        outgoing = wiki_database.fetch_outgoing_links_set(source_ids)
        outgoing = filter_single_titles(outgoing, id_to_title)

        all_links = incoming.union(outgoing)
        double_links = incoming.intersection(outgoing)
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
    return set(filter(lambda id:id in id_to_title and count_title_words(id_to_title[id]) == 1, page_ids))


def get_multi_links(page_scores):
    multi_links = set(map(lambda item:item[0], filter(lambda item:item[1] >= 3, page_scores.items())))
    return multi_links


def get_pair_links(term_links):
    print("PAIR LINKS")
    terms = term_utils.get_terms()
    all_pair_links = set()

    pairs = math.comb(len(terms), 2)
    with tqdm(total=pairs) as pbar:
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

                pbar.update(1)
    return all_pair_links


def insert_pages(target_links, term_links):
    page_extracts_database.drop_indexes()
    for link in tqdm(target_links):
        insert_page(link, term_links)
    page_extracts_database.commit()
    page_extracts_database.create_indexes()


def insert_page(page_id, term_links):
    for term in term_utils.get_terms():
        if term not in NEIGHBORS_ONLY or page_id in term_links[term]:
            for synonym in get_synonyms(term):
                page_extracts_database.insert_term_page(term, synonym, page_id)


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

    insert_pages(target_links, term_links)