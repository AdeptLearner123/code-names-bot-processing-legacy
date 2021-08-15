import progressbar
import math
import time

from utils.term_pages import TERM_PAGES
from utils.term_synonyms import get_synonyms
from utils import wiki_database
from utils import title_utils
from page_extraction import page_extracts_database

DOUBLE_LINKS = 20
PAIR_LINKS = 10

def get_links(terms):
    print("GET LINKS")
    link_scores = {}
    links = {}
    double_links = {}
    
    bar = progressbar.ProgressBar(maxval=len(terms), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in terms:
        term_link_scores, term_links, term_double_links = get_term_links(term)
        links[term] = term_links
        double_links[term] = term_double_links
        for page_id in term_link_scores:
            if page_id in link_scores:
                link_scores[page_id] += term_link_scores[page_id]
            else:
                link_scores[page_id] = term_link_scores[page_id]
        i += 1
        bar.update(i)
    bar.finish()
    return links, double_links, link_scores


def get_term_links(term):
    source_titles = TERM_PAGES[term]
    source_ids = wiki_database.get_ids_set(source_titles)
    source_ids = wiki_database.get_redirected_ids(source_ids)

    term_link_scores = {}
    for source_id in source_ids:
        term_link_scores[source_id] = 1
    
    first_links, double_links = expand_link_scores(term_link_scores, source_ids)
    second_links, second_double_links = expand_link_scores(term_link_scores, first_links)
    return term_link_scores, first_links, double_links


def expand_link_scores(term_link_scores, source_ids):
    links, directions = wiki_database.fetch_all_links(source_ids)
    link_ids = set()
    double_link_ids = set()

    for source_id in links:
        for link_id in links[source_id]:
            score = term_link_scores[source_id] / 10
            is_double = (source_id, link_id) in directions and (link_id, source_id) in directions
            if is_double:
                score *= 2
            if link_id not in term_link_scores or term_link_scores[link_id] < score:
                term_link_scores[link_id] = score
                link_ids.add(link_id)
                if is_double:
                    double_link_ids.add(link_id)
    
    return link_ids, double_link_ids


def get_top_double_links(double_links, link_scores, id_to_title, term_target_pages):
    print("DOUBLE Links")
    all_double_links = set()
    
    bar = progressbar.ProgressBar(maxval=len(term_target_pages), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in term_target_pages:
        term_double_links = get_top_pages(double_links[term], link_scores, id_to_title, DOUBLE_LINKS)
        term_target_pages[term].update(term_double_links)
        print("{0}: {1}".format(term, len(term_double_links)))
        all_double_links.update(term_double_links)
        i += 1
        bar.update(i)
    bar.finish()
    print("TOTAL: {0}".format(len(all_double_links)))
    return all_double_links


def get_top_pair_links(term_links, link_scores, id_to_title, term_target_pages):
    print("PAIR LINKS")
    terms = list(term_target_pages.keys())
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
            pair_links = get_top_pages(links, link_scores, id_to_title, PAIR_LINKS)
            term_target_pages[term1].update(pair_links)
            term_target_pages[term2].update(pair_links)
            all_pair_links.update(pair_links)
            print("{0} | {1}: {2}".format(term1, term2, len(pair_links)))

            iter += 1
            bar.update(iter)
    
    bar.finish()
    print("TOTAL: {0}".format(len(all_pair_links)))
    return all_pair_links


def get_top_pages(links, link_scores, id_to_title, count):
    double_link_scores = []
    for link_id in links:
        if link_id not in id_to_title:
            continue
        link_title = id_to_title[link_id]
        title_word_count = title_utils.count_title_words(link_title)
        double_link_scores.append((link_title, link_scores[link_id], title_word_count))

    # First sort ascending by link score, then descending by title word count
    double_link_scores.sort(key=lambda x: (x[1], -x[2]), reverse=True)
    return list(map(lambda x: x[0], double_link_scores[:count]))


def insert_term_pages(term, pages):
    term_synonyms = get_synonyms(term)
    for page in pages:
        for synonym in term_synonyms:
            page_extracts_database.insert_term_page(term, synonym, page)
    page_extracts_database.commit()


def job(terms):
    print("TITLES DICT")
    id_to_title = wiki_database.get_all_titles_dict()
    links, double_links, link_scores = get_links(terms)

    term_target_pages = {}
    for term in terms:
        term_target_pages[term] = set()

    top_double_links = get_top_double_links(double_links, link_scores, id_to_title, term_target_pages)
    top_pair_links = get_top_pair_links(links, link_scores, id_to_title, term_target_pages)
    top_links = top_double_links.union(top_pair_links)
    print("TOTAL LINKS: {0}".format(len(top_links)))

    print("INSERTING")
    bar = progressbar.ProgressBar(maxval=len(TERM_PAGES), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in term_target_pages:
        insert_term_pages(term, term_target_pages[term])
        i += 1
        bar.update(i)
    bar.finish()


def job_all():
    start_time = time.time()
    job(list(TERM_PAGES.keys()))
    print("--- %s seconds ---" % (time.time() - start_time))