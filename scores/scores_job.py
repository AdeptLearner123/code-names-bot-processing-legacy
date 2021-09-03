from tqdm import tqdm
import time
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

from utils import wiki_database
from page_extraction import page_extracts_database
from utils.title_utils import extract_title_clues
from utils.title_utils import count_title_words
from scores import scores_database
from utils import term_utils

def get_link_strength_and_str(directions, id_1, id_2):
    outgoing = (id_1, id_2) in directions
    incoming = (id_2, id_1) in directions
    if incoming and outgoing:
        return 2, '<->'
    elif incoming:
        return 1, '<-'
    elif outgoing:
        return 1, '->'
    else:
        return 0, '|'


def count_links_dict(links_dict):
    total = 0
    for id in links_dict:
        total += len(links_dict[id])
    return total


def output_scores(term):
    print("Counting: " + term)
    paths = {}
    scores = {}

    for synonym in term.get_synonyms_without_term(term):
        words = synonym.split('_')
        score = 1 / len(words)
        for word in words:
            scores[word] = score
            paths[word] = ""

    source_titles = term_utils.get_disambiguation_sources(term)
    source_ids = wiki_database.get_ids_set(source_titles)
    source_id_redirect_origins = {}
    redirected_source_ids = set()
    for source_id in source_ids:
        redirected_id = wiki_database.get_redirected_id(source_id)
        source_id_redirect_origins[redirected_id] = source_id
        redirected_source_ids.add(redirected_id)
    page_counts = page_extracts_database.get_term_page_counts(term)

    lemmatizer = WordNetLemmatizer()
    count = len(page_counts)

    print("Count: {0}".format(count))
    with tqdm(total=count) as pbar:
        for title in page_counts:
            term_count = page_counts[title]
            if term_count == 0:
                continue

            title_words = extract_title_clues(title, term)
            # We need to count title words separately since we should include term and stopwords in divisor.
            title_words_count = count_title_words(title)
            title_words = set(map(lambda x:x.upper(), title_words))
            if len(title_words) == 0:
                continue

            score = 1 - 0.7 ** term_count
            score /= title_words_count

            for word in title_words:
                word_lower = word.lower()
                term_lower = term.lower()
                if term_lower in word_lower or lemmatizer.lemmatize(word_lower) == term_lower:
                    continue

                if word not in scores or scores[word] < score:
                    scores[word] = score
                    paths[word] = title
            pbar.update(1)

    with tqdm(total=len(source_titles)) as pbar:
        for title in source_titles:
            word_counts = page_extracts_database.get_title_counts(title)
            for word in word_counts:
                score = 1 - 0.7 ** word_counts[word]
                if word not in scores or scores[word] < score:
                    scores[word] = score
                    paths[word] = title            
            pbar.update(1)

    print("Inserting: " + str(len(scores)))
    with tqdm(total=len(scores)) as pbar:
        for clue in scores:
            scores_database.insert_term_clue(term, clue, scores[clue], paths[clue])
            pbar.update(1)
    scores_database.commit()


def output_scores_job():
    start_time = time.time()

    print("Get all id to title")
    for term in term_utils.get_terms():
        output_scores(term)
    
    print("--- %s seconds ---" % (time.time() - start_time))