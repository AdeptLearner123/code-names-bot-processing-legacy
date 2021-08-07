import re
from nltk.stem.porter import *
from urllib.request import urlopen
from urllib import parse
import json
from bs4 import BeautifulSoup
from utils import extract_clue_word
import unidecode
from socket import timeout
import sys

#URL_PREFIX = 'https://en.wikipedia.org/wiki/'
URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='

def count_terms(page_title, target_term):
    term_counts, excerpts = count_terms_multi(page_title, [target_term])
    return term_counts[target_term], excerpts[target_term]


def count_terms_multi(page_title, target_terms):
    # Returns a map of counts for each target term.
    # If a term has n words, gives 1/n for each occurrence of the word.
    
    text = download_text(page_title)
    if text is None:
        return None, None
    sentences = get_sentences(text)
    term_words = get_term_words(target_terms)
    sentence_counts = count_words(term_words, sentences)
    term_counts = agg_term_counts(sentence_counts, term_words)
    excerpts = extract_excerpt(page_title, sentences, sentence_counts, term_words)
    return term_counts, excerpts


def agg_term_counts(sentence_counts, term_words):
    term_counts = {}
    for term in term_words:
        term_counts[term] = 0
    for sentence_count in sentence_counts:
        for term in sentence_count:
            term_counts[term] += sentence_count[term]
    return term_counts


def count_words(term_words, sentences):
    stemmer = PorterStemmer()
    sentence_counts = []
    for sentence in sentences:
        sentence_counts.append(count_sentence_terms(stemmer, sentence, term_words))
    return sentence_counts


def count_sentence_terms(stemmer, sentence, term_words):
    sentence = re.sub("[^a-zA-Z'.?!]+", " ", sentence)

    word_counts = {}
    for term in term_words:
        for word in term_words[term]:
            word_counts[word] = 0

    sentence = sentence.lower()
    sentence_words = sentence.split(' ')
    for word in sentence_words:
        if word in word_counts:
            word_counts[word] += 1
            continue
        word = stemmer.stem(word)
        if word in word_counts:
            word_counts[word] += 1
    
    term_counts = {}
    for term in term_words:
        total = 0
        for word in term_words[term]:
            total += word_counts[word]
        total /= len(term_words[term])
        term_counts[term] = total
    return term_counts


def get_term_words(target_terms):
    term_words = {}
    for term in target_terms:
        formatted_term = term
        if '_(' in formatted_term:
            index = formatted_term.index('_(')
            formatted_term = formatted_term[:index]
        formatted_term = formatted_term.lower()
        term_words[term] = []
        for word in formatted_term.lower().replace('_', ' ').split(' '):
            term_words[term].append(word)
    return term_words


def download_text(page_title):
    formatted_title = page_title.replace('\\', '')
    url = URL_PREFIX + parse.quote_plus(formatted_title)

    try:
        response = urlopen(url, timeout=10)
        data_json = json.loads(response.read())
        return list(data_json['query']['pages'].values())[0]['extract']
    except timeout:
        print('socket timed out - URL %s', url)
        return None
    except:
        print("Failed to download text: " + page_title + " " + url + " " + str(data_json))
        print("Unexpected error:", sys.exc_info()[0])
        return None


def get_sentences(html):
    # Add extra space around tags so we don't get sentences without a space by the period.
    html = html.replace('<', ' <').replace('>', '> ')
    soup = BeautifulSoup(html)
    text = soup.get_text()
    text = unidecode.unidecode(text)

    # Remove duplicate spaces
    text = re.sub(' +', ' ', text)
    text = text.replace(' ,', ',').replace(' .', '.')

    # Replace weird characters with space
    #text = re.sub("[^a-zA-Z'.?!]+", " ", text)
    
    # Convert domain (amazon.com) or title (Mr.Rogers) to _ so they don't get split
    #text = re.sub("[.][a-z]", "_", text)
    
    text = text\
        .replace('St. ', 'St.')\
        .replace('Mr. ', 'Mr.')\
        .replace('Ms. ', 'Ms.')\
        .replace('Mrs. ', 'Mrs.')\
        .replace('Dr. ', 'Dr.')
    text = text.replace('\n', '. ')
    sentences = text.split('. ')
    sentences = list(map(lambda sentence:sentence.strip(), sentences))
    #sentences = re.split(r'[!?.](?=(?:\s*\p{Lu})|\s*\z)', text)
    return sentences


def extract_excerpt(title, sentences, sentence_counts, term_words):
    clue_words = get_term_words([title])
    clue_sentence_counts = count_words(clue_words, sentences)
    term_excerpts = {}
    for term in term_words:
        term_excerpts[term] = extract_excerpt_term(sentences, sentence_counts, clue_sentence_counts, title, term)
    return term_excerpts


def extract_excerpt_term(sentences, sentence_counts, clue_sentence_counts, clue, term):
    half_excerpts = []
    for i in range(len(sentences)):
        term_count = sentence_counts[i][term]
        clue_count = clue_sentence_counts[i][clue]
        #print("Sentence: " + str(i) + " " + str(term_count) + " " + str(clue_count) + " " + term + " " + clue)
        if term_count >= 1 and clue_count >= 1:
            return sentences[i]
        elif term_count >= 1:
            half_excerpts.append(sentences[i])
    
    if len(half_excerpts) > 0:
        return half_excerpts[0]
    return ""