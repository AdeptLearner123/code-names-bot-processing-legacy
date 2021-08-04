import scorer
import wiki_database
from utils import extract_clue_word

NEGATIVE_THRESHOLD = 0.15

def best_clue(pos_terms, neg_terms):
    term_scores = get_term_scores(pos_terms, neg_terms)
    neg_scores = get_neg_scores(neg_terms, term_scores)
    clue_scores = get_clue_scores(pos_terms, neg_scores, term_scores)
    return get_best_clues(clue_scores, pos_terms), term_scores


def get_best_clues(clue_scores, pos_terms):
    clue_titles = wiki_database.get_titles_dict(clue_scores.keys())

    clue_scores_list = []
    for clue_id in clue_scores:
        if clue_id not in clue_titles:
            continue
        clue_word = extract_clue_word(clue_titles[clue_id], pos_terms)
        if clue_word is None:
            continue
        clue_scores_list.append((clue_word, clue_scores[clue_id]))
    clue_scores_list.sort(key=lambda tup:tup[1], reverse=True)

    return clue_scores_list[:20]


def get_term_scores(pos_terms, neg_terms):
    term_scores = {}
    all_terms = []
    all_terms.extend(pos_terms)
    all_terms.extend(neg_terms)
    for term in all_terms:
        tree, scores, directions = scorer.get_scores_term(term, 2)
        term_scores[term] = (tree, scores, directions)
    return term_scores


def get_clue_scores(pos_terms, neg_scores, term_scores):
    clue_scores = {}
    for term in pos_terms:
        scores = term_scores[term][1]
        for clue_option in scores:
            if clue_option in neg_scores and (neg_scores[clue_option] >= NEGATIVE_THRESHOLD or neg_scores[clue_option] >= scores[clue_option]):
                continue
            if clue_option not in clue_scores:
                clue_scores[clue_option] = 0
            clue_scores[clue_option] += scores[clue_option]
    return clue_scores


def get_neg_scores(neg_terms, term_scores):
    neg_scores = {}
    for term in neg_terms:
        scores = term_scores[term][1]
        for clue_option in scores:
            if clue_option not in neg_scores:
                neg_scores[clue_option] = scores[clue_option]
            else:
                neg_scores[clue_option] = max(neg_scores[clue_option], scores[clue_option])
    return neg_scores


def explore_clue_generator(pos_terms, neg_terms):
    best_clues, term_scores = best_clue(pos_terms, neg_terms)
    for clue_score in best_clues:
        print(clue_score[0] + ": " + str(clue_score[1]))
    
    val = ''
    while val != 0:
        val = input("[0] Quit [1] Get Term Scores:")
        val = int(val)
        
        if val == 1:
            clue = input("Clue: ")
            clue_id = wiki_database.title_to_id(clue)
            if clue_id is None:
                print("Invalid title")
                continue
            for term in term_scores:
                scores = term_scores[term][1]
                score = "NA" if clue_id not in scores else scores[clue_id]
                print(term + ": " + str(score))


#explore_clue_generator(['Tiger', 'Octopus', 'Dinosaur'], [])
#explore_clue_generator(['PYRAMID', 'SQUARE', 'CENTER'], [])
#explore_clue_generator(['SHADOW', 'NINJA', 'SPY'], [])