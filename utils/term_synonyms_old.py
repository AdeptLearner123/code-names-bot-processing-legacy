from re import M


SYNONYMS = {
    "ALIEN": ["EXTRATERRESTRIAL"],
    "AMERICA": ["UNITED_STATES"],
    "ARM": ["WEAPON"],
    
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
    "CHECK": ["CHEQUE"],
    "CHEST": ["THORAX"],
    "CHINA": ["PORCELAIN"],
    "COLD": ["INFLUENZA", "FLU"],
    "COMIC": ["COMEDIAN"],
    "COOK": ["CHEF"],
    "COURT": ["COURTHOUSE", "COURTYARD"],
    "CRASH": ["COLLISION"],
    "CYCLE": ["BICYCLE"],

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
    "LOG": ["LOGARITHM"],

    "MOLE": ["NEVUS"],
    "MOUNT": ["MOUNTAIN"],
    
    "PANTS": ["TROUSERS"],

    "SCUBA DIVER": ["SCUBA", "DIVER"],
    "SPY": ["ESPIONAGE"],

    "TRUNK": ["TORSO"]
}

def get_synonyms(term):
    synonyms = [term]
    if term in SYNONYMS:
        synonyms.extend(SYNONYMS[term])
    return synonyms