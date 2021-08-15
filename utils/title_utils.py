from nltk.corpus import stopwords
from nltk.stem.porter import *


def trim_suffix(clue_title):
    if '_(' in clue_title:
        index = clue_title.index('_(')
        return clue_title[:index]
    return clue_title


def extract_clue_word(clue_title, term):
    clue_title = trim_suffix(clue_title)
    if '_' in clue_title:
        clue_title = clue_title.split('_')[-1]
    if clue_title.lower() == term.lower():
        return None
    return clue_title.upper()


def count_title_words(clue_title):
    clue_title = trim_suffix(clue_title)
    return clue_title.count('_') + 1


def extract_title_words(title):
    title = trim_suffix(title)
    title_words = title.split('_')
    
    stop_words = set(stopwords.words('english'))
    stop_words.update(set(["list", "de"]))
    
    cleaned_title_words = []
    for word in title_words:
        # Clean out &, "Mirmo!", "St."
        alphanumeric = [c for c in word if c.isalnum() or c == '-']
        cleaned_word = "".join(alphanumeric)
        if len(cleaned_word) > 0 and cleaned_word.lower() not in stop_words:
            cleaned_title_words.append(cleaned_word)
    
    return list(map(lambda x:x.upper(), cleaned_title_words))


def extract_title_clues(title, term):
    lower_term = term.lower()
    words = extract_title_words(title)
    stemmer = PorterStemmer()
    filtered_words = []
    for word in words:
        if word == lower_term or stemmer.stem(word) == lower_term:
            continue
        filtered_words.append(word)
    return filtered_words