import requests
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import *

url_prefix = 'https://en.wikipedia.org/wiki/'

def count_words(title, words):
    counts = {}
    for word in words:
        counts[word] = 0
        
    stemmer = PorterStemmer()
    reqs = requests.get(url_prefix + title)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    body = soup.find('div', {'id': 'bodyContent'})
    text = body.text.lower()
    text = re.sub("[^a-zA-Z']+", " ", text)
    
    for word in text.split(' '):
        word = stemmer.stem(word)
        if word in words:
            counts[word] += 1
            
    return counts