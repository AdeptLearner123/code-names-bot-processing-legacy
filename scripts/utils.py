def extract_clue_word(clue_title, terms):
    if '_(' in clue_title:
        index = clue_title.index('_(')
        clue_title = clue_title[:index]
    if '_' in clue_title:
        return None
    if clue_title.lower() in (term.lower() for term in terms):
        return None
    return clue_title