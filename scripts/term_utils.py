import wiki_database

non_disambiguations = ["SCUBA DIVER", "HIMALAYAS", "LIMOUSINE", "PANTS"]

special_tiles = {
    "ICE CREAM": "Ice_cream",
    "SCUBA DIVER": "Scuba_diving",
}


def to_page_title(term):
    title = ''

    if term in special_tiles:
        title = special_tiles[term]
    else:
        words = term.split(' ')
        words = map(lambda word: word.capitalize(), words)
        title = '_'.join(words)
    
    if term not in non_disambiguations:
        title += "_(disambiguation)"
    
    return title


def is_disambiguation(term):
    return term not in non_disambiguations


def get_term_source_pages(term):
    title = to_page_title(term)
    id = wiki_database.title_to_id(title)
    if not is_disambiguation(term):
        return [id]

    link_ids = wiki_database.fetch_links_set([id])
    link_titles = wiki_database.get_titles_set(link_ids)
    link_ids = wiki_database.get_ids_set(link_titles)
    return link_ids


def verify_term_to_page_title():
    f = open("terms.txt", "r")
    terms = f.read().splitlines()
    titles = list(map(lambda term: to_page_title(term), terms))
    title_to_id = wiki_database.get_ids_dict(titles)
    print("Valid pages: " + str(len(title_to_id)))
    for title in titles:
        if title not in title_to_id:
            print("Missing: " + title)