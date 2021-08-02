import requests
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import *
from urllib.request import urlopen
from urllib import parse
import json

#URL_PREFIX = 'https://en.wikipedia.org/wiki/'
URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='

def count_terms(page_title, target_term):
    return count_terms_multi(page_title, [target_term])[target_term.lower()]


def count_terms_multi(page_title, target_terms):
    # Returns a map of counts for each target term.
    # If a term has n words, gives 1/n for each occurrence of the word.
    
    text = download_text(page_title)
    text = format_text(text)
    term_words, word_counts = init_word_counts(target_terms)
    count_words(word_counts, text)
    term_counts = agg_term_counts(term_words, word_counts)

    return term_counts


def agg_term_counts(term_words, word_counts):
    term_counts = {}
    for term in term_words:
        total = 0
        for word in term_words[term]:
            total += word_counts[word]
        total /= len(term_words[term])
        term_counts[term] = total
    return term_counts


def count_words(word_counts, text):
    stemmer = PorterStemmer()
    for word in text.split(' '):
        word = word.lower()
        if word in word_counts:
            word_counts[word] += 1
            continue
        word = stemmer.stem(word)
        if word in word_counts:
            word_counts[word] += 1


def init_word_counts(target_terms):
    term_words = {}
    word_counts = {}

    for term in target_terms:
        term = term.lower()
        term_words[term] = []
        for word in term.lower().replace('_', ' ').split(' '):
            term_words[term].append(word)
            word_counts[word] = 0
    return term_words, word_counts


"""
def download_text(page_title):
    reqs = requests.get(URL_PREFIX + page_title)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    body = soup.find('div', {'id': 'bodyContent'})
    return body.text
"""


def download_text(page_title):
    url = URL_PREFIX + parse.quote_plus(page_title)

    response = urlopen(url)
    data_json = json.loads(response.read())
    if 'query' not in data_json:
        return ''
    query_json = data_json['query']
    if 'pages' not in query_json:
        return ''
    pages_json = query_json['pages']
    if len(pages_json) <= 0:
        return ''
    page_json = list(pages_json.values())[0]
    if 'extract' not in page_json:
        return ''
    return page_json['extract']


def format_text(text):
    text = text.lower()
    text = re.sub("[^a-zA-Z']+", " ", text)
    return text