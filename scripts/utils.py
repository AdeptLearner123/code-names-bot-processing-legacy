def trim_suffix(clue_title):
    if '_(' in clue_title:
        index = clue_title.index('_(')
        return clue_title[:index]
    return clue_title


def extract_clue_word(clue_title, term):
    clue_title = trim_suffix(clue_title)
    if '_' in clue_title:
        clue_title = clue_title.split('_')[-1]
    if clue_title.lower() == term.lower():
        return None
    return clue_title.upper()


def count_title_words(clue_title):
    clue_title = trim_suffix(clue_title)
    return clue_title.count('_') + 1