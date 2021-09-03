from re import S
from sqlite3.dbapi2 import TimeFromTicks
import spacy
nlp = spacy.load("en_core_web_sm")
from tqdm import tqdm
import time

from utils import wiki_database
from utils.title_utils import extract_title_words
from page_extraction import page_extractor
from page_extraction import page_extracts_database
from page_downloads import page_downloads_database
from page_downloads import page_downloader
from nltk.stem import WordNetLemmatizer
from utils import term_utils

def get_source_page_counts(title):
    page_id = wiki_database.title_to_id(title)
    page_id = wiki_database.get_redirected_id(page_id)
    
    id = wiki_database.title_to_id(title)
    link_ids = wiki_database.fetch_outgoing_links_set([id])
    words = page_ids_to_words(link_ids)

    text = page_downloads_database.get_content(title)
    noun_counts, noun_chunks, noun_excerpts = page_extractor.extract_noun_chunks(text)
    word_counts = dict()
    word_excerpts = dict()
    for word in words:
        if word in noun_counts:
            word_counts[word] = noun_counts[word]
            if len(noun_excerpts[word]) > 0:
                sorted_excerpts = sorted(noun_excerpts[word], key=lambda sentence:sentence.lower().count(title.lower()), reverse=True)
                word_excerpts[word] = sorted_excerpts[0]
    return word_counts, word_excerpts


def page_ids_to_words(ids):
    titles = wiki_database.get_titles_set(ids)
    titles = map(lambda title:extract_title_words(title), titles)
    titles = filter(lambda words:len(words) == 1, titles)
    titles = map(lambda words:words[-1], titles)
    titles = set(titles)
    return titles


def get_counts(term):
    noun_counts = {}
    noun_excerpts = {}
    for title in term_utils.get_disambiguation_sources(term):
        title_noun_counts, title_word_excerpts = get_source_page_counts(title)
        for noun in title_noun_counts:
            if noun not in noun_counts or noun_counts[noun] < title_noun_counts[noun]:
                noun_counts[noun] = title_noun_counts[noun]
                noun_excerpts[noun] = title_word_excerpts[noun]
    return noun_counts, noun_excerpts


def job():
    start_time = time.time()

    all_sources = term_utils.get_all_sources()
    page_downloader.download_multi_threaded(all_sources)
    
    with tqdm(total=len(all_sources)) as pbar:
        for term in term_utils.get_terms():
            for title in term_utils.get_disambiguation_sources(term):
                title_noun_counts, title_word_excerpts = get_source_page_counts(title)
                for noun in title_noun_counts:
                    page_extracts_database.insert_term_page_count_excerpt(term, noun.upper(), title, title_noun_counts[noun], title_word_excerpts[noun], True)
                page_extracts_database.commit()
                pbar.update(1)

    print("--- %s seconds ---" % (time.time() - start_time))