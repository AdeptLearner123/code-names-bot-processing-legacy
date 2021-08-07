import sample_board
from term_pages import TERM_PAGES
import wiki_database
import wiki_term_counter
import progressbar
import os.path

def output_counts(term):
    link_ids = get_link_ids(term)
    link_titles = wiki_database.get_titles_set(link_ids)
    print("Counting: " + term + " " + str(len(link_titles)))
    file_name = get_file_name(term)
    if os.path.isfile(file_name):
        print("Found existing titles")
        link_titles = link_titles.difference(get_counted_links(term))

    print("Total: " + str(len(link_titles)))

    f = open("csv_output/" + term + ".csv", "a")
    if not os.path.isfile(file_name):
        print("Writing header")
        f.write("page,count")
    bar = progressbar.ProgressBar(maxval=len(link_titles), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    link_titles = list(link_titles)
    for i in range(len(link_titles)):
        bar.update(i + 1)
        link_title = link_titles[i]
        count = wiki_term_counter.count_terms(link_title, term)
        f.write(link_title + "," + str(count) + "\n")
    bar.finish()
    f.close()


def get_link_ids(term):
    source_titles = TERM_PAGES[term]
    source_ids = wiki_database.get_ids_set(source_titles)
    target_ids = wiki_database.fetch_all_links_set(source_ids)
    #target_ids = wiki_database.fetch_incoming_links_set(source_ids)
    #target_ids = wiki_database.fetch_outgoing_links_set(source_ids)
    return target_ids


def get_counted_links(term):
    f = open(get_file_name(term), "r")
    titles = set()
    rows = f.read().splitlines()
    for i in range(1, len(rows)):
        titles.add(rows[i].split(',')[0])
    return titles


def get_file_name(term):
    return "csv_output/" + term + ".csv"


for term in sample_board.get_all_terms():
    print("Term: " + term + " " + str(len(get_link_ids(term))))
    #output_counts(term)