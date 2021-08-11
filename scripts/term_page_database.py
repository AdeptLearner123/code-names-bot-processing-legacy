import sqlite3

con = sqlite3.connect('term_page.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS term_page (
                term TEXT NOT NULL,
                word TEXT NOT NULL,
                title TEXT NOT NULL,
                count REAL DEFAULT NULL,
                excerpt TEXT DEFAULT NULL,
                CONSTRAINT term_word_title_unique UNIQUE (term, word, title)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_title_index ON term_page (term, title);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_index ON term_page (term);
        """
    )


def insert_term_page(term, word, title):
    cur.execute("SELECT * FROM term_page WHERE term=? AND word=? AND title=?;", [term, word, title])
    if cur.fetchone() is not None:
        return
    cur.execute("INSERT INTO term_page (term, word, title) VALUES (?, ?, ?)", [term, word, title])


def commit():
    con.commit()


def insert_count_excerpt(word, title, count, excerpt):
    cur.execute("UPDATE term_page SET count=?, excerpt=? WHERE word=? AND title=?;", [count, excerpt, word, title])
    con.commit()


def get_term_words(term):
    cur.execute("SELECT DISTINCT word FROM term_page WHERE term=?", [term])
    words = []
    for row in cur.fetchall():
        words.append(row[0])
    return words


def clear():
    cur.execute("DELETE from term_page")
    con.commit()
    cur.execute("VACUUM")
    con.commit()