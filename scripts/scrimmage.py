from term_pages import TERM_PAGES
from random import sample
import clue_generator

all_terms = set(TERM_PAGES.keys())

def sample_terms(size):
    global all_terms
    s = sample(all_terms, size)
    all_terms = all_terms.difference(set(s))
    return s

blue = sample_terms(8)
red = sample_terms(9)
black = sample_terms(1)
blank = sample_terms(7)

def print_board():
    print("BLUE: {0}".format('   '.join(list(blue))))
    print("RED: {0}".format('   '.join(list(red))))
    print("BLACK: {0}".format('   '.join(list(black))))
    print("BLANK: {0}".format('   '.join(list(blank))))


def print_clue():
    clue = clue_generator.best_clue(blue, red + black + blank, 1)[0]
    print("CLUE: {0} ({1})   {2}".format(clue[0], clue[2], clue[1]))


def guess():
    val = ''
    while val != 0:
        val = input("[0] Stop [1] Guess [2] Explore:")
        val = int(val)
        if val == 1:
            clue = input("Clue: ")
            blue.remove(clue)
            red.remove(clue)
            black.remove(clue)
            blank.remove(clue)
            print_board()
        elif val == 2:
            clue = input("Clue: ")
            clue_generator.explore_clue(clue, blue, red + black + blank)


print_board()
while len(blue) > 0:
    print_clue()
    guess()