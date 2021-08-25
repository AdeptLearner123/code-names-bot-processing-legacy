from utils.term_pages import TERM_PAGES
from utils import wiki_database
from utils.title_utils import extract_title_words
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database

def get_source_page_counts(title):
    page_id = wiki_database.title_to_id(title)
    page_id = wiki_database.get_redirected_id(page_id)
    first_outgoing_ids = wiki_database.fetch_outgoing_links_set([page_id])
    second_outgoing_ids = wiki_database.fetch_outgoing_links_set(first_outgoing_ids)
    
    allowed_prefix = extract_title_words(title)[0].upper()
    first_words = page_ids_to_words(first_outgoing_ids, allowed_prefix)
    second_words = page_ids_to_words(second_outgoing_ids, allowed_prefix)
    simple_noun_counts = page_extractor.extract_noun_counts(page_downloads_database.get_content(title, True))
    filtered_second_words = set(filter(lambda word:word in simple_noun_counts, second_words))

    noun_counts = page_extractor.extract_noun_counts(page_downloads_database.get_content(title))
    words = first_words.union(filtered_second_words)
    print("Words: {0} {1} {2} {3}".format(len(first_words), len(second_words), len(filtered_second_words), len(words)))
    word_counts = dict()
    for word in words:
        score = 0
        if word in simple_noun_counts:
            score += simple_noun_counts[word] * 3
        if word in noun_counts:
            score += noun_counts[word]
        if score > 0:
            word_counts[word] = score
    return word_counts


def page_ids_to_words(ids, allowed_prefix):
    titles = wiki_database.get_titles_set(ids)
    titles = map(lambda title:extract_title_words(title), titles)
    titles = filter(lambda words:len(words) == 1 or (len(words) == 2 and words[0].upper() == allowed_prefix), titles)
    titles = map(lambda words:words[-1], titles)
    titles = set(titles)
    return titles


def get_counts(term):
    noun_counts = {}
    page_downloader.download_multi(TERM_PAGES[term], True)
    for title in TERM_PAGES[term]:
        title_noun_counts = get_source_page_counts(title)
        for noun in title_noun_counts:
            if noun not in noun_counts or noun_counts[noun] < title_noun_counts[noun]:
                noun_counts[noun] = title_noun_counts[noun]
    return noun_counts