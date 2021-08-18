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


def output_scores(term, id_to_title):
    print("Counting: " + term)
    paths = {}
    scores = {}
    page_scores = {}
    page_paths = {}

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

    source_links, directions_1 = wiki_database.fetch_all_links(redirected_source_ids)
    incoming_links = wiki_database.fetch_incoming_links_set(redirected_source_ids)
    citation_titles = citations.get_term_citations(term)
    link_1_ids = set()

    link_1_count = count_links_dict(source_links)
    print("1st degree: " + str(link_1_count))
    bar = progressbar.ProgressBar(maxval=link_1_count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    for source_id in source_links:
        source_title = id_to_title[source_id_redirect_origins[source_id]]
        source_counts = page_extracts_database.get_title_counts(source_title)

        for source_word in source_counts:
            source_score = 1 - 0.7 ** source_counts[source_word]
            if source_word not in scores or scores[source_word] < source_score:
                scores[source_word] = source_score
                paths[source_word] = source_title

        for link_1_id in source_links[source_id]:
            if link_1_id not in id_to_title:
                continue
            link_1_title = id_to_title[link_1_id]
            # If the only connection between term and page is a citation
            if link_1_id not in incoming_links and link_1_title in citation_titles:
                continue
            link_1_words = extract_title_clues(link_1_title, term)
            # We need to count title words separately since we should include term and stopwords in divisor.
            link_1_words_count = count_title_words(link_1_title)
            link_1_words = set(map(lambda x:x.upper(), link_1_words))
            if len(link_1_words) == 0:
                continue

            term_count = 0
            if link_1_title in page_counts:
                term_count = page_counts[link_1_title]

            link_strength, link_str = get_link_strength_and_str(directions_1, source_id, link_1_id)
            path_str = source_title + link_str + link_1_title

            score = 1 - 0.7 ** term_count
            score /= link_1_words_count

            for word in link_1_words:
                word_lower = word.lower()
                term_lower = term.lower()
                if word_lower == term_lower or stemmer.stem(word_lower) == term_lower or lemmatizer.lemmatize(word_lower) == term_lower:
                    continue

                if word not in scores or scores[word] < score:
                    scores[word] = score
                    paths[word] = path_str

            page_scores[link_1_id] = score
            page_paths[link_1_id] = path_str

            # We only want to score second-degree links of crawled articles.
            # Otherwise there will be too many.
            if term_count > 0:
                link_1_ids.add(link_1_id)
            i += 1
            bar.update(i)
    bar.finish()

    link_1_links = wiki_database.fetch_double_links(link_1_ids)

    link_2_count = count_links_dict(link_1_links)
    print("1st degree to expand: " + str(len(link_1_ids)))
    print("2nd degree: " + str(link_2_count))
    bar = progressbar.ProgressBar(maxval=link_2_count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()

    for link_1_id in link_1_links:
        link_1_score = page_scores[link_1_id]
        for link_2_id in link_1_links[link_1_id]:
            if link_2_id not in id_to_title:
                continue
            if link_2_id in link_1_ids:
                continue
            link_2_title = id_to_title[link_2_id]
            link_2_words = extract_title_clues(link_2_title, term)
            link_2_words_count = count_title_words(link_2_title)
            if len(link_2_words) != 1:
                continue
            #link_strength, link_str = get_link_strength_and_str(directions_2, link_1_id, link_2_id)
            #score = link_1_score / 10 * link_strength
            score = link_1_score / 5
            score /= link_2_words_count

            for word in link_2_words:
                if word not in scores or scores[word] < score:
                    scores[word] = score
                    #paths[word] = page_paths[link_1_id] + link_str + link_2_title
                    paths[word] = page_paths[link_1_id] + '<->' + link_2_title

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
    id_to_title = wiki_database.get_all_titles_dict()
    for term in TERM_PAGES:
        output_scores(term, id_to_title)
    
    print("--- %s seconds ---" % (time.time() - start_time))