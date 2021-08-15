import sqlite3
import time
import progressbar

from utils.term_pages import TERM_PAGES
from page_extraction import page_extracts_database

def transfer():
    con = sqlite3.connect('output.sqlite')
    cur = con.cursor()

    def get_entry(term, title):
        cur.execute("SELECT count, excerpt FROM term_page WHERE term=? AND title=?", [term, title])
        row = cur.fetchone()
        if row is None:
            return None, None
        return row[0], row[1]

    start_time = time.time()

    bar = progressbar.ProgressBar(maxval=len(TERM_PAGES), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in TERM_PAGES:
        empty_titles = page_extracts_database.get_empty_entries(term)
        print("{0}: {1}".format(term, len(empty_titles)))
        for empty_title in empty_titles:
            count, excerpt = get_entry(term, empty_title)
            if count is not None and excerpt is not None:
                page_extracts_database.insert_count_excerpt(term, empty_title, count, excerpt)
        i += 1
        bar.update(i)
    bar.finish()

    print("--- %s seconds ---" % (time.time() - start_time))

    print("Empty: {0} / {1}".format(page_extracts_database.count_empty_entries(), page_extracts_database.count_entries()))