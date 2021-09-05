from utils import wiki_database


def print_incoming_links(titles):
    for title in titles:
        id = wiki_database.title_to_id(title)
        print(id)
        print("{0}: {1}".format(title, len(wiki_database.fetch_incoming_links_set([id]))))