from re import M


SYNONYMS = {
    "AMERICA": ["UNITED STATES"],
    "ARM": ["WEAPON"],
    "AZTEC": ["AZTECS"],
    
    "BILL": ["INVOICE", "BEAK"],
    "BOARD": ["BLACKBOARD", "WHITEBOARD", "PLANK"],
    "BOND": ["BAIL"],
    "BOOM": ["EXPLOSION"],
    "BUCK": ["DOLLAR", "DEER"],
    "BUFFALO": ["BUBALINA", "BISON"],
    "BUG": ["HEMIPTERA", "INSECT"],

    "CAR": ["AUTOMOBILE"],
    "CENTER": ["CENTRE"],
    "CHAIR": ["CHAIRMAN", "CHAIRPERSON"],
    "CHANGE": ["IMPERMANENCE"],
    "CHECK": ["CHEQUE"],
    "CHEST": ["THORAX"],
    "CHINA": ["PORCELAIN"],
    "COLD": ["INFLUENZA", "FLU"],
    "COMIC": ["COMEDIAN"],
    "COOK": ["CHEF"],
    "COURT": ["COURTHOUSE", "COURTYARD"],
    "CRASH": ["COLLISION"],
    "CYCLE": ["BICYCLE"],
    "CZECH": ["CZECHS"],

    "DIAMOND": ["RHOMBUS"],
    "DOCTOR": ["PHYSICIAN"],
    "DRAFT": ["CONSCRIPTION"],
    "DWARF": ["MIDGET"],

    "FALL": ["AUTUMN"],
    "FIGHTER": ["COMBATANT", "WARRIOR"],
    "FIGURE": ["FIGURINE"],
    "FILE": ["DOCUMENT"],
    "FILM": ["MOVIE"],
    "FLY": ["FLIGHT"],

    "GAS": ["GASOLINE"],
    
    "JAM": ["JAMMING"],

    "KID": ["YOUTH", "CHILD"],
    "KIWI": ["KIWIFRUIT"],

    "LAB": ["LABORATORY"],
    "LINK": ["HYPERLINK"],
    "LOG": ["LOGARITHM", "LUMBER"],

    "MINT": ["MENTHA"],
    "MOLE": ["NEVUS"],
    "MOUNT": ["MOUNTAIN"],

    "PALM": ["ARECACEAE"],    
    "PANTS": ["TROUSERS"],
    "PASTE": ["ADHESIVE"],
    "PIE": ["PI"],
    "PUPIL": ["STUDENT"],

    "ROW": ["ROWING"],

    "SCUBA DIVER": ["SCUBA", "DIVER"],
    "SEAL": ["PINNIPED"],
    "SERVER": ["WAITER"],
    "SHOP": ["SHOPPING"],
    "SPELL": ["INCANTATION"],
    "SPY": ["ESPIONAGE"],
    "STICK": ["TWIG"],
    "SUB": ["SUBMARINE", "SUBSTITUTE TEACHER"],

    "TIE": ["NECKTIE"],
    "TRUNK": ["TORSO"],
    "THEATER": ["THEATRE"],
    "THIEF": ["THEFT"],

    "UNDERTAKER": ["FUNERAL DIRECTOR"],

    "VET": ["VETERINARIAN", "VETERAN"],
    "WASHER": ["DISH WASHER", "WASHING MACHINE"]
}

def get_synonyms(term):
    synonyms = [term]
    if term in SYNONYMS:
        synonyms.extend(SYNONYMS[term])
    return synonyms