from tqdm import tqdm
import time

from utils import wiki_database
from utils.title_utils import extract_title_words
from page_extraction import page_extractor
from page_extraction import page_extracts_database
from page_downloads import page_downloads_database
from page_downloads import page_downloader
from utils import term_utils

def get_source_page_counts(id):
    title = wiki_database.id_to_title(id)
    link_ids = wiki_database.fetch_outgoing_links_set([id])
    words = page_ids_to_words(link_ids)

    text = page_downloads_database.get_content(id)
    if text is None:
        return None, None
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
    titles = map(lambda words:words[0], titles)
    titles = set(titles)
    return titles


def job():
    start_time = time.time()

    all_source_ids = term_utils.get_all_source_ids()
    page_downloader.download_multi(all_source_ids)
    
    with tqdm(total=len(all_source_ids)) as pbar:
        for term in term_utils.get_terms():
            for id in term_utils.get_source_ids(term):
                source_page_counts, source_page_excerpts = get_source_page_counts(id)
                if source_page_counts is None:
                    continue
                for noun in source_page_counts:
                    page_extracts_database.insert_term_page_count_excerpt(term, noun.upper(), id, source_page_counts[noun], source_page_excerpts[noun], True)
                page_extracts_database.commit()
                pbar.update(1)

    print("--- %s seconds ---" % (time.time() - start_time))