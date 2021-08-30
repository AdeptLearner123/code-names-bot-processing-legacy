from utils.term_synonyms import get_synonyms
from nltk.stem.wordnet import WordNetLemmatizer
from utils.title_utils import extract_title_words
from utils import wiki_database
#from utils.term_pages_old import TERM_PAGES

TITLE_OVERRIDE = {
    "NEW YORK": "New_York",
    "LOCH NESS": "Loch_Ness"
}

SOURCE_OVERRIDE = {
    "HIMALAYAS": ["Himalayas"],
    "LIMOUSINE": ["Limousine"],
    "PANTS": ["Trousers"],
    "SCUBA DIVER": ["Scuba_diving"]
}

TERMS = list(open('terms.txt', 'r').read().splitlines())
#TERMS = list(TERM_PAGES.keys())

def get_terms():
    return TERMS


def validate_source_title(title, term):
    title = title.lower()
    if 'disambiguation' in title or 'list' in title:
        return False
    lemmatizer = WordNetLemmatizer()
    title_words = extract_title_words(title)
    title_words = set(filter(lambda word:lemmatizer.lemmatize(word), title_words))
    for synonym in get_synonyms(term):
        for word in synonym.split(' '):
            if word.upper() in title_words:
                return True
    return False


def get_term_sources(term):
    if term in SOURCE_OVERRIDE:
        return SOURCE_OVERRIDE[term]
    disambiguation_title = get_disambiguation_title(term)
    disambiguation_id = wiki_database.title_to_id(disambiguation_title)
    disambiguation_id = wiki_database.get_redirected_id(disambiguation_id)
    source_ids = wiki_database.fetch_outgoing_links_set([disambiguation_id])
    source_titles = wiki_database.get_titles_set(source_ids)
    print(source_titles)
    source_titles = set(filter(lambda title:validate_source_title(title, term), source_titles))
    return source_titles


def get_disambiguation_title(term):
    title = term.capitalize().replace(' ', '_') if term not in TITLE_OVERRIDE else TITLE_OVERRIDE[term]
    return "{0}_(disambiguation)".format(title)