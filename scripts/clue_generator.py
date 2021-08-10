import scores_database
import wiki_database
from utils import extract_clue_word

NEGATIVE_THRESHOLD = 2.0

def best_clue(pos_terms, neg_terms, count, ignore=[]):
    term_scores = get_term_scores(pos_terms, neg_terms)
    neg_scores = get_neg_scores(neg_terms, term_scores)
    clue_scores, clue_counts = get_clue_scores(pos_terms, neg_scores, term_scores)
    return get_best_clues(clue_scores, clue_counts, count, ignore)


def get_best_clues(clue_scores, clue_counts, count, ignore=[]):
    clue_scores_list = []
    for clue in clue_scores:
        if clue not in ignore:
            clue_scores_list.append((clue, clue_scores[clue], clue_counts[clue]))
    clue_scores_list.sort(key=lambda tup:tup[1], reverse=True)

    return clue_scores_list[:count]


def get_term_scores(pos_terms, neg_terms):
    term_scores = {}
    for term in pos_terms + neg_terms:
        term_scores[term] = scores_database.get_scores(term)
    return term_scores


def get_clue_scores(pos_terms, neg_scores, term_scores):
    clue_scores = {}
    clue_counts = {}
    for term in pos_terms:
        scores = term_scores[term]
        for clue_option in scores:
            if clue_option in neg_scores and (neg_scores[clue_option] >= NEGATIVE_THRESHOLD or neg_scores[clue_option] >= scores[clue_option]):
                continue
            if clue_option not in clue_scores:
                clue_scores[clue_option] = 0
                clue_counts[clue_option] = 0
            clue_scores[clue_option] += scores[clue_option]
            clue_counts[clue_option] += 1
    return clue_scores, clue_counts


def get_neg_scores(neg_terms, term_scores):
    neg_scores = {}
    for term in neg_terms:
        scores = term_scores[term]
        for clue_option in scores:
            if clue_option not in neg_scores:
                neg_scores[clue_option] = scores[clue_option]
            else:
                neg_scores[clue_option] = max(neg_scores[clue_option], scores[clue_option])
    return neg_scores


def print_clue_term(term, clue):
    term_clue = scores_database.get_term_clue(term, clue)
    if term_clue is None:
        print("Term: {0} N/A".format(term))
    else:
        print("Term: {0} Score: {1} Path: {2}".format(term, term_clue[0], term_clue[1]))


def explore_clue(clue, pos_terms, neg_terms):
    print("POSITIVE")
    for term in pos_terms:
        print_clue_term(term, clue)
    print("NEGATIVE")
    for term in neg_terms:
        print_clue_term(term, clue)


def explore_clue_generator(pos_terms, neg_terms):
    best_clues = best_clue(pos_terms, neg_terms, 20)
    for clue_score in best_clues:
        print("{0}: {1} ({2})".format(clue_score[0], clue_score[1], clue_score[2]))
    
    val = ''
    while val != 0:
        val = input("[0] Quit [1] Get Term Scores:")
        val = int(val)
        
        if val == 1:
            clue = input("Clue: ")
            explore_clue(clue, pos_terms, neg_terms)


#explore_clue_generator(['LION', 'OCTOPUS', 'DINOSAUR'], [])
#explore_clue_generator(['PYRAMID', 'SQUARE', 'CENTER'], [])
#explore_clue_generator(['SHADOW', 'NINJA', 'SPY'], [])
#explore_clue_generator(['POUND', 'PART'], [])