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

def get_source_page_counts(title, term):
    page_id = wiki_database.title_to_id(title)
    page_id = wiki_database.get_redirected_id(page_id)
    
    text = page_extractor.format_text(page_downloads_database.get_content(title))

    first_outgoing_ids = wiki_database.fetch_outgoing_links_set([page_id])
    second_outgoing_ids = wiki_database.fetch_outgoing_links_set(first_outgoing_ids)
    
    first_words = page_ids_to_words(first_outgoing_ids)
    second_words = page_ids_to_words(second_outgoing_ids)
    words = first_words.union(second_words)

    print("Words: {0} {1} {2}".format(len(first_words), len(second_words), len(words)))

    root_counts, root_chunks = page_extractor.extract_noun_chunks(page_downloads_database.get_content(title))
    word_counts = dict()
    word_chunks = dict()
    for word in words:
        if word in root_counts:
            word_counts[word] = root_counts[word]
            word_chunks[word] = root_chunks[word]
    return word_counts, word_chunks

    lemmatizer = WordNetLemmatizer()

    chunk_counts = dict()
    chunk_roots = dict()
    doc = nlp(text)

    for chunk in doc.noun_chunks:
        nc = chunk.text.lower()
        #if ' ' in nc or nc.upper() not in words:
        #  continue
        if nc not in chunk_counts:
            chunk_counts[nc] = 1
        else:
            chunk_counts[nc] += 1
        chunk_roots[nc] = lemmatizer.lemmatize(chunk.root.text)

    bar = progressbar.ProgressBar(maxval=len(words), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()
    word_counts = dict()
    word_chunks = dict()
    for word in words:
        for chunk in chunk_counts:
            if word == chunk_roots[chunk].upper():
                if word not in word_counts or chunk_counts[chunk] < word_counts[word]:
                    word_counts[word] = chunk_counts[chunk]
                    word_chunks[word] = chunk
        i += 1
        bar.update(i)
    bar.finish()

    return word_counts, word_chunks


def page_ids_to_words(ids):
    titles = wiki_database.get_titles_set(ids)
    titles = map(lambda title:extract_title_words(title), titles)
    titles = filter(lambda words:len(words) == 1, titles)
    titles = map(lambda words:words[-1], titles)
    titles = set(titles)
    return titles


def get_counts(term):
    noun_counts = {}
    noun_chunks = {}
    for title in TERM_PAGES[term]:
        title_noun_counts, title_noun_chunks = get_source_page_counts(title, TimeFromTicks)
        for noun in title_noun_counts:
            if noun not in noun_counts or noun_counts[noun] < title_noun_counts[noun]:
                noun_counts[noun] = title_noun_counts[noun]
                noun_chunks[noun] = title_noun_chunks[noun]
    return noun_counts, noun_chunks