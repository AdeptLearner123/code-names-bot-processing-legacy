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
import inflect
p = inflect.engine()

from utils.nlp_utils import get_ne_chunks

VALID_POS = set(["VB", "NN", "JJ"])

def count_terms(page_title, target_term, text):
    term_counts, excerpts = count_terms_multi(page_title, [target_term], text)
    return term_counts[target_term], excerpts[target_term]


def count_terms_multi(page_title, target_terms, text):
    sentences = get_sentences(text)
    sentence_words_list, sentence_ne_list = get_sentence_words(sentences)
    ne_tokenized, ne_counts, ne_sentence_counts = aggregate_ne_list(sentence_ne_list)
    word_counts, word_sentence_counts = aggregate_word_list(sentence_words_list)

    _, _, title_sentence_counts = count_term(page_title, sentences, word_counts, word_sentence_counts, ne_tokenized, ne_counts, ne_sentence_counts)
    term_counts = {}
    term_excerpts = {}
    for term in target_terms:
        counted_term, count, sentence_counts = count_term(term, sentences, word_counts, word_sentence_counts, ne_tokenized, ne_counts, ne_sentence_counts)
        if counted_term is None:
            term_counts[term] = 0
            term_excerpts[term] = None
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
            if re.compile(r'[0-9]').search(nc):
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


def get_sentence_words(sentences):
    sentence_words_list = []
    sentence_ne_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        sentence_words = filter(lambda token: token.tag_[0:2] in VALID_POS and not token.tag_[1] == "NNP", doc)
        sentence_words = list(map(lambda token: (token.lemma_, token.tag_[0:2]), sentence_words))
        sentence_words_list.append(sentence_words)

        sentence_ne_list.append(list(map(lambda ent:ent.text, doc.ents)))

    return sentence_words_list, sentence_ne_list


def count_term(term, sentences, word_counts, word_sentence_counts, ne_tokenized, ne_counts, ne_sentence_counts):
    if ' ' in term:
        return count_multi_word_term(term, sentences)
    return count_single_word_term(term, word_counts,word_sentence_counts, ne_tokenized, ne_counts, ne_sentence_counts)


def count_single_word_term(term, word_counts, word_sentence_counts, ne_tokenized, ne_counts, ne_sentence_counts):
    valid_pos = set(filter(lambda pos: (term.lower(), pos) in word_counts, VALID_POS))
    max_pos = max(valid_pos, key=lambda pos:word_counts.get((term.lower(), pos))) if len(valid_pos) > 0 else None

    valid_nes = set(filter(lambda ne:term.lower() in ne_tokenized[ne], ne_tokenized.keys()))
    max_ne = max(valid_nes, key=ne_counts.get) if len(valid_nes) > 0 else None

    if max_pos is not None:
        max_word_tag = (term.lower(), max_pos)
        max_word_tag_sentence_counts = list(map(lambda word_count:word_count[max_word_tag] if max_word_tag in word_count else 0, word_sentence_counts))

        if max_ne is None or word_counts[max_word_tag] > ne_counts[max_ne]:
            return term.lower(), word_counts[max_word_tag], max_word_tag_sentence_counts
    
    if max_ne is not None:
        max_ne_sentence_counts = list(map(lambda ne_count:ne_count[max_ne] if max_ne in ne_count else 0, ne_sentence_counts))
        return max_ne, ne_counts[max_ne], max_ne_sentence_counts
    
    return None, 0, [0] * len(word_sentence_counts)


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
    return half_excerpt


def aggregate_ne_list(sentence_ne_list):
    ne_tokenized = {}
    ne_counts = {}
    ne_sentence_counts = []
    for ne_list in sentence_ne_list:
        curr_ne_counts = {}
        for ne in ne_list:
            if ne not in ne_tokenized:
                ne_tokenized[ne] = set(word.lower() for word in word_tokenize(ne))

            if ne in curr_ne_counts:
                curr_ne_counts[ne] += 1
            else:
                curr_ne_counts[ne] = 1

            if ne in ne_counts:
                ne_counts[ne] += 1
            else:
                ne_counts[ne] = 1
        ne_sentence_counts.append(curr_ne_counts)
    return ne_tokenized, ne_counts, ne_sentence_counts


def aggregate_word_list(sentence_word_list):
    word_counts = {}
    word_sentence_counts = []
    for word_list in sentence_word_list:
        curr_word_counts = {}
        for word_tag in word_list:
            if word_tag in curr_word_counts:
                curr_word_counts[word_tag] += 1
            else:
                curr_word_counts[word_tag] = 1

            if word_tag in word_counts:
                word_counts[word_tag] += 1
            else:
                word_counts[word_tag] = 1
        word_sentence_counts.append(curr_word_counts)
    return word_counts, word_sentence_counts