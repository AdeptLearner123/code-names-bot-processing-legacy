from utils.term_synonyms import get_synonyms
from nltk.stem.wordnet import WordNetLemmatizer
from utils.title_utils import extract_title_words
from utils.title_utils import trim_suffix
from utils.title_utils import has_suffix
from utils.title_utils import get_suffix
from utils import wiki_database
from utils.term_synonyms import get_synonyms
from utils.term_source_supplements import SOURCE_SUPPLEMENTS
from pyinflect import getAllInflections

TITLE_OVERRIDE = {
    "NEW YORK": "New_York",
    "LOCH NESS": "Loch_Ness"
}

IGNORE_DISMAMBIGUATION = { 'LIMOUSINE', 'HIMALAYAS', 'PANTS', "SCUBA DIVER" }

TERMS = list(open('terms.txt', 'r').read().splitlines())
#IGNORE_SUFFIX_WORDS = set(['film', 'tv', 'song', 'album', 'radio'])

def get_terms():
    return TERMS


def validate_source_title(page_id, title, term):
    title_lower = title.lower()
    if 'disambiguation' in title_lower or 'list' in title_lower:
        return False

    title_trimmed = trim_suffix(title)
    synonyms = get_synonyms(term)
    if title_trimmed.upper().replace('_', ' ') in synonyms:
        if title_trimmed.isupper():
            return False
        if not has_suffix(title):
            return True
        else:
            #suffix = get_suffix(title).lower()
            #for ignore_suffix_word in IGNORE_SUFFIX_WORDS:
             #   if ignore_suffix_word in suffix:
              #      return False
            return True
    return False


def get_disambiguation_sources(term):
    if term in IGNORE_DISMAMBIGUATION:
        return set()
    disambiguation_title = get_disambiguation_title(term)
    disambiguation_id = wiki_database.title_to_id(disambiguation_title)
    disambiguation_id = wiki_database.get_redirected_id(disambiguation_id)
    source_ids = wiki_database.fetch_outgoing_links_set([disambiguation_id])
    source_id_to_title = wiki_database.get_titles_dict(source_ids)
    source_titles = set(filter(lambda item:validate_source_title(item[0], item[1], term), source_id_to_title.items()))
    source_titles = set(map(lambda item:item[1], source_titles))
    return source_titles


def get_sources(term):
    sources = set()
    if term in SOURCE_SUPPLEMENTS:
        sources.update(set(SOURCE_SUPPLEMENTS[term]))
    if term not in IGNORE_DISMAMBIGUATION:
        sources.update(get_disambiguation_sources(term))
    return sources


def get_source_ids(term):
    sources = get_sources(term)
    return wiki_database.get_ids_set(sources)


def get_disambiguation_title(term):
    if term in IGNORE_DISMAMBIGUATION:
        return None
    title = term.capitalize().replace(' ', '_') if term not in TITLE_OVERRIDE else TITLE_OVERRIDE[term]
    return "{0}_(disambiguation)".format(title)


def get_all_sources():
    sources = set()
    for term in get_terms():
        sources.update(get_sources(term))
    return sources


def get_all_source_ids():
    sources = get_all_sources()
    return wiki_database.get_ids_set(sources)


def get_word_tag_to_pos():
    word_tag_to_term_pos = {}
    for term in get_terms():
        for synonym in get_synonyms(term):
            inflections = getAllInflections(synonym)
            for pos in inflections:
                inflected_term = inflections[pos][0].upper()
                word_tag_to_term_pos[(inflected_term, pos)] = (synonym, pos[0:2])
    return word_tag_to_term_pos