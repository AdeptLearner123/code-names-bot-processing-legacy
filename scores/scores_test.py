from scores import scores_database

positive_scores = [
    ("BOMB", "CANNON"),
    ("EUROPE", "HISTORY"),
    ("AFRICA", "PALEOLITHIC"),
    ("BAND", "GACKT"),
    ("BUFFALO", "CATTLE"),
    ("BATTERY", "CHARGE"),
    ("MAMMOTH", "ANIMAL"),
    ("BLOCK", "VOLLEYBALL"),
    ("ANGEL", "CALIFORNIA"),
    ("ALIEN", "KAIJU")
]

negative_scores = [
    ("ARM", "BAT"),
    ("BAND", "ANT"),
    ("POUND", "ANT"),
    ("BACK", "CATTLE"),
    ("BALL", "ENTREPRENEURSHIP"),
    ("ORGAN", "BASEBALL"),
    ("ORGAN", "ENTREPRENEURSHIP"),
    ("BUCK", "NATIONAL"),
    ("MOON", "MADE"),
    ("BEIJING", "HIGH"),
    ("ALIEN", "NAZI"),
    ("ALIEN", "NOUN"),
    ("ALIEN", "CROSSOVER"),
    ("AMAZON", "SWORD-AND-SANDAL"),
    ("AMBULANCE", "LONDON"),
    ("AMBULANCE", "CANBERRA"),
    ("BACK", "VOLLEYBALL"),
    ("BANK", "SYDNEY"),
    ("BAR", "BEEHIVE"),
    ("BATTERY", "FIREARM"),
    ("ARM", "MYANMAR"),
    ("BELL", "HELICOPTER"),
    ("BILL", "DISCO"),
    ("BOOM", "SUBURBS"),
    ("BOW", "POLICE"),
    ("BOX", "GUERSNEY"),
    ("BRIDGE", "DETROIT"),
    ("BRIDGE", "TURKEY"),
    ("BUCK", "VERMONT"),
    ("BUCK", "THAILAND"),
    ("BUFFALO", "SPEAR"),
    ("BUG", "ULTRAVIOLET"),
    ("CANADA", "MILLENNIAL"),
    ("CENTER", "VILNIUS"),
    ("LINK", "BIOPHILIA"),
    ("LION", "YODELING"),
    ("NINJA", "CROSSOVER"),
    ("NOVEL", "ANDROMEDA"),
    ("OCTOPUS", "PUNISHMENT"),
    ("AIR", "JUPITER")
]


def test_multi():
    file_names = ["scores #1", "scores #2", "scores #3", "scores"]
    for file_name in file_names:
        scores_database.init(file_name)
        print("TESTING: {0}".format(file_name))
        test()
        print("\n\n\n")


def test():
    print("POSITIVE ================ ")
    squared_error = 0
    for term, clue in positive_scores:
        score, path = scores_database.get_term_clue(term, clue)
        
        if score is None or path is None:
            score = 0
            path = ''
        
        squared_error += (1 - score) ** 2
        print("{0} {1}: {2}        {3}".format(term, clue, score, path))
    
    print("\n\nNEGATIVE ===============")
    for term, clue in negative_scores:
        score, path = scores_database.get_term_clue(term, clue)

        if score is None or path is None:
            score = 0
            path = ''

        squared_error += score ** 2
        print("{0} {1}: {2}        {3}".format(term, clue, score, path))
    
    squared_error /= len(positive_scores) + len(negative_scores)
    print("\n\nMean Squared Error: {0}".format(squared_error))