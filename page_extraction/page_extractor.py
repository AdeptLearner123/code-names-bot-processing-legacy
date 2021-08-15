import re
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from urllib.request import urlopen
from urllib import parse
import json
from bs4 import BeautifulSoup
import unidecode
from socket import timeout
import sys

URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='

def count_terms(page_title, target_term, text):
    term_counts, excerpts = count_terms_multi(page_title, [target_term], text)
    return term_counts[target_term], excerpts[target_term]


def count_terms_multi(page_title, target_terms, text):
    # Returns a map of counts for each target term.
    # If a term has n words, gives 1/n for each occurrence of the word.
    
    #text = download_text(page_title)
    #if text is None:
    #    return None, None
    sentences = get_sentences(text)
    term_words = get_term_words(target_terms)
    title_words = get_term_words([page_title])[page_title]
    sentence_counts, sentence_title_counts = count_words(term_words, title_words, sentences)
    term_counts = agg_term_counts(sentence_counts, term_words)
    excerpts = extract_excerpt(sentences, sentence_counts, sentence_title_counts, term_words)
    return term_counts, excerpts


def agg_term_counts(sentence_counts, term_words):
    term_counts = {}
    for term in term_words:
        term_counts[term] = 0
    for sentence_count in sentence_counts:
        for term in sentence_count:
            term_counts[term] += sentence_count[term]
    return term_counts


def count_words(term_words, title_words, sentences):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    sentence_counts = []
    sentence_title_counts = []
    for sentence in sentences:
        term_counts, title_count = count_sentence_terms(stemmer, lemmatizer, stop_words, sentence, term_words, title_words)
        sentence_counts.append(term_counts)
        sentence_title_counts.append(title_count)
    return sentence_counts, sentence_title_counts


def count_sentence_terms(stemmer, lemmatizer, stop_words, sentence, term_words, title_words):
    sentence = re.sub("[^a-zA-Z'.?!]+", " ", sentence)

    word_counts = {}
    for term in term_words:
        for word in term_words[term]:
            word_counts[word] = 0
    
    for word in title_words:
        word_counts[word] = 0

    sentence = sentence.lower()
    sentence_words = sentence.split(' ')
    for word in sentence_words:
        if word in stop_words:
            continue
        if word in word_counts:
            word_counts[word] += 1
            continue
        word_stemmed = stemmer.stem(word)
        if word_stemmed in word_counts:
            word_counts[word_stemmed] += 1
            continue
        word_lemmatized = lemmatizer.lemmatize(word)
        if word_lemmatized in word_counts:
            word_counts[word_lemmatized] += 1
    
    term_counts = {}
    for term in term_words:
        total = 0
        for word in term_words[term]:
            total += word_counts[word]
        total /= len(term_words[term])
        term_counts[term] = total
    
    title_total = 0
    for word in title_words:
        title_total += word_counts[word]
    title_total /= len(title_words)

    return term_counts, title_total


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
        print("Failed to download text: " + page_title + " " + url)
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

    text = text\
        .replace('St. ', 'St.')\
        .replace('Mr. ', 'Mr.')\
        .replace('Ms. ', 'Ms.')\
        .replace('Mrs. ', 'Mrs.')\
        .replace('Dr. ', 'Dr.')\
        .replace('Lt. ', 'Lt.')
    text = text.replace('\n', '. ')
    sentences = text.split('. ')
    sentences = list(map(lambda sentence:sentence.strip(), sentences))
    return sentences


def extract_excerpt(sentences, sentence_counts,  sentence_title_counts, term_words):
    term_excerpts = {}
    for term in term_words:
        term_excerpts[term] = extract_excerpt_term(sentences, sentence_counts, sentence_title_counts, term)
    return term_excerpts


def extract_excerpt_term(sentences, sentence_counts, clue_sentence_counts, term):
    half_excerpts = []
    for i in range(len(sentences)):
        term_count = sentence_counts[i][term]
        clue_count = clue_sentence_counts[i]
        if term_count >= 1 and clue_count >= 1:
            return sentences[i]
        elif term_count >= 1:
            half_excerpts.append(sentences[i])
    
    if len(half_excerpts) > 0:
        return half_excerpts[0]
    return ""