def convert_to_title(word):
    parts = word.split(' ')
    parts = map(lambda part: part.capitalize(), parts)
    return '_'.join(parts)


def code_name_to_title(word):
    mapper = {
        "APPLE": "Apple_(disambiguation)",
        "ICE CREAM": "Ice_cream_(disambiguation)",
        "SCUBA DIVER": "Scuba_diving",
        "LOCH NESS": "Loch_Ness"
    }

    if word in mapper:
        return mapper[word]
    return convert_to_title(word)