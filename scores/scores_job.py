import progressbar
import time
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

from utils import wiki_database
from utils.term_pages import TERM_PAGES
from utils.term_synonyms import SYNONYMS
from page_extraction import page_extracts_database
from utils.title_utils import extract_title_clues
from utils.title_utils import count_title_words
from scores import scores_database
from citations import citations

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

    if term in SYNONYMS:
        for synonym in SYNONYMS[term]:
            words = synonym.split('_')
            score = 1 / len(words)
            for word in words:
                scores[word] = score
                paths[word] = ""

    source_titles = TERM_PAGES[term]
    source_ids = wiki_database.get_ids_set(source_titles)
    source_id_redirect_origins = {}
    redirected_source_ids = set()
    for source_id in source_ids:
        redirected_id = wiki_database.get_redirected_id(source_id)
        source_id_redirect_origins[redirected_id] = source_id
        redirected_source_ids.add(redirected_id)
    page_counts = page_extracts_database.get_term_page_counts(term)

    count = len(page_counts)
    print("Count: {0}".format(count))
    bar = progressbar.ProgressBar(maxval=count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()

    lemmatizer = WordNetLemmatizer()

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

        i += 1
        bar.update(i)
    bar.finish()

    bar = progressbar.ProgressBar(maxval=len(source_titles), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for title in source_titles:
        word_counts = page_extracts_database.get_title_counts(title)
        for word in word_counts:
            score = 1 - 0.7 ** word_counts[word]
            if word not in scores or scores[word] < score:
                scores[word] = score
                paths[word] = title            
        i += 1
        bar.update(i)
    bar.finish()

    print("Inserting: " + str(len(scores)))
    bar = progressbar.ProgressBar(maxval=len(scores), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()
    for clue in scores:
        scores_database.insert_term_clue(term, clue, scores[clue], paths[clue])
        i += 1
        bar.update(i)
    scores_database.commit()
    bar.finish()


def output_scores_job():
    start_time = time.time()

    print("Get all id to title")
    for term in TERM_PAGES:
        output_scores(term)
    
    print("--- %s seconds ---" % (time.time() - start_time))