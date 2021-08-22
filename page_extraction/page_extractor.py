from bs4 import BeautifulSoup
import unidecode
import re
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

from utils.nlp_utils import get_ne_chunks


def count_terms(page_title, target_term, text):
    term_counts, excerpts = count_terms_multi(page_title, [target_term], text)
    return term_counts[target_term], excerpts[target_term]


def count_terms_multi(page_title, target_terms, text):
    sentences = get_sentences(text)
    sentence_nouns_list, sentence_ne_list = get_sentence_nouns(sentences, target_terms)

    _, _, title_sentence_counts = count_term(page_title, sentences, sentence_nouns_list, sentence_ne_list)
    term_counts = {}
    term_excerpts = {}
    for term in target_terms:
        counted_term, count, sentence_counts = count_term(term, sentences, sentence_nouns_list, sentence_ne_list)
        term_counts[term] = count
        term_excerpts[term] = get_excerpt(sentence_counts, title_sentence_counts, sentences)
    return term_counts, term_excerpts


def get_sentences(html):
    # Add extra space around tags so we don't get sentences without a space by the period.
    html = html.replace('<', ' <').replace('>', '> ')
    soup = BeautifulSoup(html)
    text = soup.get_text()
    text = unidecode.unidecode(text)

    # Remove duplicate spaces
    text = re.sub(' +', ' ', text)
    text = text.replace(' ,', ',').replace(' .', '.')

    text = text.replace('\n', '. ')
    sentences = sent_tokenize(text)
    sentences = list(map(lambda sentence:sentence.strip(), sentences))
    return sentences


def get_sentence_nouns(sentences, terms):
    lemmatizer = WordNetLemmatizer()
    sentence_nouns_list = []
    sentence_ne_list = []
    terms_set = set(map(lambda term:term.lower(), terms))

    for sentence in sentences:
        pos_words = pos_tag(word_tokenize(sentence))

        sentence_nouns = filter(lambda word_pos: word_pos[1].startswith('NN') and not word_pos[1] == "NNP", pos_words)
        sentence_nouns = list(map(lambda noun_pos:lemmatizer.lemmatize(noun_pos[0]), sentence_nouns))
        sentence_nouns_list.append(sentence_nouns)

        should_chunk = False
        sentence_proper_nouns = filter(lambda word_pos: word_pos[1].startswith('NNP'), pos_words)
        for proper_noun, pos in sentence_proper_nouns:
            for proper_noun_word in word_tokenize(proper_noun):
                if proper_noun_word.lower() in terms_set:
                    should_chunk = True
                    break
        if should_chunk:
            sentence_ne_list.append(get_ne_chunks(pos_words))
        else:
            sentence_ne_list.append([])

    return sentence_nouns_list, sentence_ne_list


def count_term(term, sentences, sentence_nouns_list, sentence_ne_list):
    if ' ' in term:
        return count_multi_word_term(term, sentences)
    return count_single_word_term(term, sentence_nouns_list, sentence_ne_list)


def count_single_word_term(term, sentence_nouns_list, sentence_ne_list):
    common_noun_count = 0
    common_noun_sentence_counts = []
    for nouns_list in sentence_nouns_list:
        count = len(list(filter(lambda noun:noun.lower() == term.lower(), nouns_list)))
        common_noun_count += count
        common_noun_sentence_counts.append(count)

    ne_counts = {}
    ne_sentence_counts = []
    for ne_list in sentence_ne_list:
        filtered_ne_list = list(filter(lambda ne:term.lower() in (word.lower() for word in word_tokenize(ne)), ne_list))
        curr_ne_counts = {}
        for ne in filtered_ne_list:
            if ne in curr_ne_counts:
                curr_ne_counts[ne] += 1
            else:
                curr_ne_counts[ne] = 1

            if ne in ne_counts:
                ne_counts[ne] += 1
            else:
                ne_counts[ne] = 1
        ne_sentence_counts.append(curr_ne_counts)

    max_ne = max(ne_counts, key=ne_counts.get) if len(ne_counts) > 0 else None

    if max_ne is None or common_noun_count > ne_counts[max_ne]:
        return term.lower(), common_noun_count, common_noun_sentence_counts
    
    max_ne_sentence_counts = list(map(lambda ne_count:ne_count[max_ne] if max_ne in ne_count else 0, ne_sentence_counts))
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
    return half_excerpt