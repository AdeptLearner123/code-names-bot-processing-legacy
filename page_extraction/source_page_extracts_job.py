from sqlite3.dbapi2 import TimeFromTicks
import spacy
nlp = spacy.load("en_core_web_sm")
import progressbar

from utils.term_pages import TERM_PAGES
from utils import wiki_database
from utils.title_utils import extract_title_words
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database
from nltk.stem import WordNetLemmatizer

def get_source_page_counts(title):
    page_id = wiki_database.title_to_id(title)
    page_id = wiki_database.get_redirected_id(page_id)
    
    lemmatizer = WordNetLemmatizer()
    id = wiki_database.title_to_id(title)
    link_ids = wiki_database.fetch_outgoing_links_set([id])
    titles = wiki_database.get_titles_set(link_ids)
    titles = map(lambda title:lemmatizer.lemmatize(extract_title_words(title)[-1]), titles)
    words = set(titles)

    print("Words: {0}".format(len(words)))

    text = page_downloads_database.get_content(title)
    noun_counts, noun_chunks = page_extractor.extract_noun_chunks(text)
    word_counts = dict()
    for word in words:
        if word in noun_counts:
            word_counts[word] = noun_counts[word]
    return word_counts


def page_ids_to_words(ids):
    titles = wiki_database.get_titles_set(ids)
    titles = map(lambda title:extract_title_words(title), titles)
    titles = filter(lambda words:len(words) == 1, titles)
    titles = map(lambda words:words[-1], titles)
    titles = set(titles)
    return titles


def get_counts(term):
    noun_counts = {}
    for title in TERM_PAGES[term]:
        title_noun_counts = get_source_page_counts(title)
        for noun in title_noun_counts:
            if noun not in noun_counts or noun_counts[noun] < title_noun_counts[noun]:
                noun_counts[noun] = title_noun_counts[noun]
    return noun_counts