import sqlite3

con = sqlite3.connect('output.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS term_page (
                term TEXT NOT NULL,
                title TEXT NOT NULL,
                count REAL NOT NULL,
                excerpt TEXT NOT NULL,
                CONSTRAINT term_title_unique UNIQUE (term, title)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_title_index ON term_page (term, title);
        """
    )


def insert_term_page(term, title, count, excerpt):
    cur.execute("SELECT * FROM term_page WHERE term=? AND title=?;", [term, title])
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO term_page (term, title, count, excerpt) VALUES(?,?,?,?);", [term, title, count, excerpt])
    else:
        cur.execute("UPDATE term_page SET count=?, excerpt=? WHERE term=? AND title=?;", [count, excerpt, term, title])
    con.commit()


def get_missing_pages(term, titles):
    query = "SELECT title FROM term_page WHERE term=? AND title IN ({0});".format(placeholder_list(titles))
    cur.execute(query, [term] + list(titles))
    titles_set = set(titles)
    existing_titles = set()
    for row in cur.fetchall():
        existing_titles.add(row[0])
    return titles_set.difference(existing_titles)


def placeholder_list(list):
    return ', '.join('?' for i in list)


def count_term_entries(term):
    query = "SELECT COUNT() FROM term_page WHERE term=?"
    cur.execute(query, [term])
    return cur.fetchone()[0]


def sample_term_pages(term, count):
    query = "SELECT * FROM term_page WHERE term=? LIMIT ?"
    cur.execute(query, [term, count])
    return cur.fetchall()


def get_term_page_counts(term):
    query = "SELECT title, count FROM term_page WHERE term=?"
    cur.execute(query, [term])
    counts = {}
    for row in cur.fetchall():
        counts[row[0]] = row[1]
    return counts


def count_all_entries():
    query = "SELECT COUNT() FROM term_page"
    cur.execute(query)
    return cur.fetchone()[0]


def sample_all_entries(count):
    query = "SELECT * FROM term_page LIMIT ?"
    cur.execute(query, [count])
    return cur.fetchall()


def count_empties():
    cur.execute("SELECT COUNT() FROM term_page WHERE excerpt IS NULL OR excerpt=''")
    return cur.fetchone()[0]


def get_terms():
    cur.execute("SELECT DISTINCT term FROM term_page")
    return list(map(lambda row:row[0], cur.fetchall()))


def get_entry(term, title):
    cur.execute("SELECT count, excerpt FROM term_page WHERE term=? AND title=?", [term, title])
    return cur.fetchone()


def delete_entry(term, title):
    cur.execute("DELETE FROM term_page WHERE term=? AND title=?", [term, title])
    con.commit()