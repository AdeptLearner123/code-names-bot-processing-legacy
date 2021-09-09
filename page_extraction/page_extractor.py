from bs4 import BeautifulSoup
import unidecode
import re
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()
from nltk.stem import WordNetLemmatizer
import spacy
nlp = spacy.load("en_core_web_sm")
from utils.nlp_utils import get_ne_chunks
from pyinflect import getAllInflections

from utils import term_utils
from utils.title_utils import trim_suffix

VALID_POS = {"VB", "NN", "JJ"}
WORD_TAG_TO_TERM_POS = term_utils.get_word_tag_to_pos()
NUMBERS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"}

def count_terms(page_title, target_term, text):
    term_counts, excerpts = count_terms_multi(page_title, [target_term], text)
    return term_counts[target_term], excerpts[target_term]


def count_terms_multi(page_title, terms, text):
    page_title = trim_suffix(page_title)

    sentences = get_sentences(text)
    sentence_words_list, sentence_ne_list = get_sentence_words(sentences, terms)

    target_terms = [page_title.upper()] + list(terms)
    term_ne, ne_counts, ne_sentence_counts = aggregate_ne_list(sentence_ne_list, target_terms)
    term_pos_counts, term_pos_sentence_counts = aggregate_word_list(sentence_words_list, target_terms)

    _, _, title_sentence_counts = count_term(page_title.upper(), sentences, term_ne, ne_counts, ne_sentence_counts, term_pos_counts, term_pos_sentence_counts)
    term_counts = {}
    term_excerpts = {}
    for term in terms:
        counted_term, count, sentence_counts = count_term(term, sentences, term_ne, ne_counts, ne_sentence_counts, term_pos_counts, term_pos_sentence_counts)
        if counted_term is None:
            term_counts[term] = 0
            term_excerpts[term] = ''
            continue
        term_counts[term] = count
        term_excerpts[term] = get_excerpt(sentence_counts, title_sentence_counts, sentences)
    return term_counts, term_excerpts


def extract_noun_chunks(text):
    root_counts = dict()
    root_chunks = dict()
    root_excerpts = dict()
    lemmatizer = WordNetLemmatizer()
    sentences = get_sentences(text)

    for sentence in sentences:
        doc = nlp(sentence)
        for chunk in doc.noun_chunks:
            nc = chunk.text.lower()
            root = lemmatizer.lemmatize(chunk.root.text).upper()
            if noun_chunk_has_number(nc):
                continue
            if root not in root_counts:
                root_counts[root] = 1
                root_chunks[root] = set([nc])
                root_excerpts[root] = [sentence]
            else:
                root_counts[root] += 1
                root_chunks[root].add(nc)
                root_excerpts[root].append(sentence)
    return root_counts, root_chunks, root_excerpts


def noun_chunk_has_number(noun_chunk):
        if re.compile(r'[0-9]').search(noun_chunk):
            return True
        for word in noun_chunk.split(' '):
            if word.lower() in NUMBERS:
                return True
        return False

def get_sentences(html):
    text = format_text(html)
    sentences = sent_tokenize(text)
    sentences = list(map(lambda sentence:sentence.strip(), sentences))
    return sentences


def format_text(html):
    # Add extra space around tags so we don't get sentences without a space by the period.
    html = html.replace('<', ' <').replace('>', '> ')
    soup = BeautifulSoup(html)
    text = soup.get_text()
    text = unidecode.unidecode(text)

    # Remove duplicate spaces
    text = re.sub(' +', ' ', text)
    text = text.replace(' ,', ',').replace(' .', '.')
    text = text.replace('\n', '. ')
    return text


def get_sentence_words(sentences, terms):
    sentence_words_list = []
    sentence_ne_list = []

    for sentence in sentences:
        tagged_sentence = tagger.tag(word_tokenize(sentence))
        sentence_words = filter(lambda word_tag: word_tag[1][0:2] in VALID_POS and not word_tag[1] == "NNP", tagged_sentence)
        sentence_words = list(map(lambda word_tag: (word_tag[0].upper(), word_tag[1]), sentence_words))
        sentence_words_list.append(sentence_words)

        # Optimize by checking if any term is contained in a proper noun before extracting named entities.
        proper_nouns = list(filter(lambda word_tag: word_tag[1] == "NNP" and word_tag[0].upper() in terms, tagged_sentence))
        if len(proper_nouns) > 0:
            ne_list = get_ne_chunks(tagged_sentence)
            ne_list = list(map(lambda ne:ne.upper(), ne_list))
            sentence_ne_list.append(ne_list)
        else:
            sentence_ne_list.append([])

    return sentence_words_list, sentence_ne_list

def count_term(term, sentences, term_ne, ne_counts, ne_sentence_counts, term_pos_counts, term_pos_sentence_counts):
    if ' ' in term:
        return count_multi_word_term(term, sentences)
    return count_single_word_term(term, term_ne, ne_counts, ne_sentence_counts, term_pos_counts, term_pos_sentence_counts)


def count_single_word_term(term, term_ne, ne_counts, ne_sentence_counts, term_pos_counts, term_pos_sentence_counts):
    max_pos = max(VALID_POS, key=lambda pos:term_pos_counts[(term, pos)])
    max_pos_sentence_counts = term_pos_sentence_counts[(term, max_pos)]

    max_ne = None
    if (len(term_ne[term]) > 0):
        max_ne = max(term_ne[term], key=lambda ne:ne_counts[ne])
        max_ne_sentence_counts = ne_sentence_counts[max_ne]

    if max_ne is None or ne_counts[max_ne] < term_pos_counts[(term, max_pos)]:
        return max_pos, term_pos_counts[(term, max_pos)], max_pos_sentence_counts
    return max_ne, ne_counts[max_ne], max_ne_sentence_counts


def count_multi_word_term(term, sentences):
    total_count = 0
    sentence_counts = []
    for sentence in sentences:
        count = sentence.lower().count(term.lower())
        total_count += count
        sentence_counts.append(count)
    return term.lower(), total_count, sentence_counts


def get_excerpt(term_sentence_counts, title_sentence_counts, sentences):
    half_excerpt = None
    for i in range(len(term_sentence_counts)):
        if title_sentence_counts[i] > 0 and term_sentence_counts[i] > 0:
            return sentences[i]
        if term_sentence_counts[i] > 0 and half_excerpt is None:
            half_excerpt = sentences[i]
    return half_excerpt if half_excerpt is not None else ''


def aggregate_ne_list(sentence_ne_list, terms):
    term_ne = {}
    for term in terms:
        term_ne[term] = set()

    processed_ne = set()
    ne_counts = {}
    ne_sentence_counts = {}
    for ne_list in sentence_ne_list:
        for ne in ne_list:
            ne = ne.upper()
            if ne in processed_ne:
                continue
            ne_words = [word.upper() for word in word_tokenize(ne)]
            for ne_word in ne_words:
                if ne_word in terms:
                    term_ne[ne_word].add(ne)
            processed_ne.add(ne)

    for ne in processed_ne:
        ne_counts[ne] = 0
        ne_sentence_counts[ne] = []
        for ne_list in sentence_ne_list:
            count = ne_list.count(ne)
            ne_counts[ne] += count
            ne_sentence_counts[ne].append(count)

    return term_ne, ne_counts, ne_sentence_counts


def aggregate_word_list(sentence_word_list, terms):
    sentence_term_pos_list = get_sentence_term_pos_list(sentence_word_list)

    term_pos_counts = {}
    term_pos_sentence_counts = {}

    for term in terms:
        for pos in VALID_POS:
            term_pos_counts[(term, pos)] = 0
            term_pos_sentence_counts[(term, pos)] = []
            for term_pos_list in sentence_term_pos_list:
                count = term_pos_list_count(term_pos_list, term, pos)
                term_pos_counts[(term, pos)] += count
                term_pos_sentence_counts[(term, pos)].append(count)

    return term_pos_counts, term_pos_sentence_counts


def get_sentence_term_pos_list(sentence_word_list):
    sentence_term_pos_list = []
    for word_list in sentence_word_list:
        term_pos_list = []
        for word_tag in word_list:
            if word_tag in WORD_TAG_TO_TERM_POS:
                term_pos_list.append(WORD_TAG_TO_TERM_POS[word_tag])
        sentence_term_pos_list.append(term_pos_list)
    return sentence_term_pos_list


def term_pos_list_count(term_pos_list, term, pos):
    return term_pos_list.count((term, pos))