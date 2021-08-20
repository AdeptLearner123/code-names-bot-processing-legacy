SYNONYMS = {
    "ALIEN": ["EXTRATERRESTRIAL"],
    "AMERICA": ["UNITED_STATES"],

    "BILL": ["INVOICE", "BEAK"],
    "BOARD": ["BLACKBOARD", "WHITEBOARD", "PLANK"],
    "BOND": ["BAIL"],
    "BOOM": ["EXPLOSION"],
    "BUCK": ["DOLLAR", "DEER"],
    "BUFFALO": ["BUBALINA", "BISON"],
    "BUG": ["HEMIPTERA", "INSECT"],

    "CENTER": ["CENTRE"],


    "LINK": ["HYPERLINK"],

    "PANTS": ["TROUSERS"],

    "SPY": ["ESPIONAGE"],

    "TRUNK": ["TORSO"]
}

def get_synonyms(term):
    synonyms = [term]
    if term in SYNONYMS:
        synonyms.extend(SYNONYMS[term])
    return synonyms