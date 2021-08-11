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


def extract_title_words(title):
    title = trim_suffix(title)
    title_words = title.split('_')
    cleaned_title_words = []
    for word in title_words:
        alphanumeric = [c for c in word if c.isalnum()]
        cleaned_title_words.append("".join(alphanumeric))
    return cleaned_title_words