from utils.term_synonyms import get_synonyms
from tqdm import tqdm
import time

from utils import wiki_database
from page_extraction import page_extracts_database
from utils.title_utils import extract_title_words
from scores import scores_database
from utils import term_utils
from pagerank import pagerank_database


def output_scores(term, id_to_title, pageranks):
    print("Counting: " + term)
    paths = {}
    scores = {}
    excerpts = {}

    get_synonym_scores(term, paths, scores, excerpts)
    get_link_page_scores(term, paths, scores, excerpts, id_to_title, pageranks)
    get_source_page_scores(term, paths, scores, excerpts, id_to_title, pageranks)

    print("Inserting: {0}".format(len(scores)))
    term_id = term_utils.term_to_id(term)
    for clue in tqdm(scores):
        if term not in clue:
            scores_database.insert_term_clue(term_id, clue, scores[clue], paths[clue], excerpts[clue])
    scores_database.commit()


def get_synonym_scores(term, paths, scores, excerpts):
    for synonym in get_synonyms(term):
        if term not in synonym:
            words = synonym.split('_')
            score = 1 / len(words)
            for word in words:
                scores[word] = score
                paths[word] = ""
                excerpts[word] = ""


def get_link_page_scores(term, paths, scores, excerpts, id_to_title, pageranks):
    term_page_counts = page_extracts_database.get_term_page_counts(term, False)
    page_counts = {}
    page_excerpts = {}
    for word, page_id, count, excerpt in term_page_counts:
        if count is None:
            continue
        if page_id not in page_counts or page_counts[page_id] < count:
            page_counts[page_id] = count
            page_excerpts[page_id] = excerpt

    print("Count: {0}".format(len(page_counts)))
    for page_id in page_counts:
        term_count = page_counts[page_id]
        if term_count == 0:
            continue

        title = id_to_title[page_id]
        title_words = extract_title_words(title)
        if len(title_words) != 1:
            continue

        clue = title_words[0]
        scores[clue] = get_score(pageranks[page_id], term_count)
        paths[clue] = title
        excerpts[clue] = page_excerpts[page_id]


def get_source_page_scores(term, paths, scores, excerpts, id_to_title, pageranks):
    term_page_counts = page_extracts_database.get_term_page_counts(term, True)
    word_counts = {}
    word_page = {}
    word_excerpts = {}
    for word, page_id, count, excerpt in tqdm(term_page_counts):
        if word not in word_counts or word_counts[word] < count:
            word_counts[word] = count
            word_page[word] = page_id
            word_excerpts[word] = excerpt

    for word in word_counts:
        score = get_score(pageranks[word_page[word]], word_counts[word])
        if word not in scores or scores[word] < score:
            scores[word] = score
            paths[word] = id_to_title[word_page[word]]
            excerpts[word] = word_excerpts[word]


def get_score(pagerank, word_count):
    link_confidence = 1 - 0.7 ** word_count
    page_confidence = min(1, pagerank / 6)
    return link_confidence * page_confidence


def output_scores_job():
    start_time = time.time()

    print("Get all id to title")
    id_to_title = wiki_database.get_all_titles_dict()

    print("Get page ranks")
    pageranks = pagerank_database.get_pageranks()

    for term in term_utils.get_terms():
        output_scores(term, id_to_title, pageranks)

    print("--- %s seconds ---" % (time.time() - start_time))