import random

from utils.term_pages import TERM_PAGES
from game import clue_generator


def sample_terms(size, all_terms):
    s = random.sample(all_terms, size)
    for word in s:
        all_terms.remove(word)
    return s


def play(seed):
    # Make all terms a sorted list so random can sample consistently with same seed.
    random.seed(seed)
    all_terms = list(TERM_PAGES.keys())
    all_terms.sort()

    blue = sample_terms(8, all_terms)
    red = sample_terms(9, all_terms)
    black = sample_terms(1, all_terms)
    blank = sample_terms(7, all_terms)
    
    #blue = ["BED", "APPLE", "DINOSAUR", "STATE", "AMAZON", "ANTARCTICA", "LION", "MOON"]
    #blue = ["AZTEC", "NOVEL", "ANTARCTICA"]
    #red = ["PART", "SNOW", "EUROPE", "AGENT", "NINJA", "BUCK", "ARM", "CENTER", "TRUNK"]
    #black = ["PANTS"]
    #blank = ["ANGEL", "POUND", "PIANO", "PIN", "ALPS", "MAMMOTH", "OCTOPUS"]
    #blue = ["PYRAMID", "CENTER", "SQUARE"]
    #red = []
    #black = []
    #blank = []

    starting_positive = blue.copy()
    starting_negative = red + black + blank
    given_clues = []
    history = []

    def print_board():
        print("BLUE: {0}".format('   '.join(list(blue))))
        print("RED: {0}".format('   '.join(list(red))))
        print("BLACK: {0}".format('   '.join(list(black))))
        print("BLANK: {0}".format('   '.join(list(blank))))


    def print_board_player():
        print("WORDS: {0}".format('    '.join(sorted(blue + red + black + blank))))
        print("BLUE: {0}".format(len(blue)))
        print("RED: {0}".format(len(red)))
        print("BLACK: {0}".format(len(black)))
        print("BLANK: {0}".format(len(blank)))


    def print_clue():
        clue, score, count, terms = clue_generator.best_clue(blue, red + black + blank, 1, given_clues)[0]
        given_clues.append(clue)
        print("Given clues: " + str(given_clues))
        print("CLUE: {0} ({1})   {2}".format(clue, count, score))
        return clue, count, terms


    def guess():
        val = ''
        guesses = []
        while val != 0:
            val = input("[0] Stop [1] Guess [2] Explain [3] Explain All [4] Explain All Verboes:")
            val = int(val)
            if val == 0:
                print()
            if val == 1:
                guess = input("GUESS: ")
                if guess in blue:
                    blue.remove(guess)
                elif guess in red: 
                    red.remove(guess)
                elif guess in black:
                    black.remove(guess)
                elif guess in blank:
                    blank.remove(guess)
                guesses.append(guess)
                #print_board()
                print_board_player()
            elif val == 2:
                clue = input("Clue: ")
                clue_generator.explore_clue(clue, blue, red + black + blank)
            elif val == 3:
                clue = input("Clue: ")
                clue_generator.explore_clue(clue, starting_positive, starting_negative)
            elif val == 4:
                clue = input("Clue: ")
                clue_generator.explore_clue(clue, starting_positive, starting_negative, True)
        return guesses


    def print_history():
        score = 0
        for clue, count, terms, guesses in history:
            terms_set = set(terms)
            guesses_set = set(guesses)
            correct = len(guesses_set.intersection(terms_set))
            incorrect = len(guesses_set.difference(terms_set))
            print("CLUE: {0}   CORRECT: {1}   INCORRECT: {2}   TERMS: {3}   GUESSED: {4}".format(clue, correct, incorrect, terms, guesses))
            score += correct - incorrect
        print("SCORE: {0}".format(score / len(history)))

    print_board_player()
    #print_board()
    while len(blue) > 0:
        clue, count, terms = print_clue()
        guesses = guess()
        history.append((clue, count, terms, guesses))
    
    print_history()