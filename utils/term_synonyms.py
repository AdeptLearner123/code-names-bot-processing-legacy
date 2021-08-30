from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def get_synonyms(term):
    lemmatizer = WordNetLemmatizer()
    syns = wordnet.synsets(term.lower())
    synonyms = set()
    for ss in syns:
        if ss.pos() == 'n':
            for synonym in ss.lemma_names():
                unrelated_lemmas = list(filter(lambda ss2:ss2.pos() == 'n' and (len(ss2.lemma_names()) > 1 and lemmatizer.lemmatize(term.lower()) not in ss2.lemma_names()), wordnet.synsets(synonym)))
                if len(unrelated_lemmas) == 0:
                    synonyms.add(synonym)
    return synonyms