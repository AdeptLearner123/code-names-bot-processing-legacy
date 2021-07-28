import requests
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import *

url_prefix = 'https://en.wikipedia.org/wiki/'

def count_words(title, words):
    # Loch_Ness => Loch, Ness
    word_parts = {}
    parts = []

    for word in words:
        word = word.lower()
        word_parts[word] = []
        for part in word.lower().replace('_', ' ').split(' '):
            word_parts[word].append(part)
            parts.append(part)
    
    counts = {}
    for part in parts:
        counts[part] = 0
        
    stemmer = PorterStemmer()
    reqs = requests.get(url_prefix + title)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    body = soup.find('div', {'id': 'bodyContent'})
    text = body.text.lower()
    text = re.sub("[^a-zA-Z']+", " ", text)
    
    for word in text.split(' '):
        word = word.lower()
        if word in parts:
            counts[word] += 1
            continue
        word = stemmer.stem(word)
        if word in parts:
            counts[word] += 1
    
    word_counts = {}
    for word in word_parts:
        total = 0
        for part in word_parts[word]:
            total += counts[part]
        total /= len(word_parts[word])
        word_counts[word] = total

    return word_counts