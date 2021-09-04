from tqdm import tqdm
import sqlite3

from utils import wiki_database
from utils import term_utils

con = sqlite3.connect('page_extraction/page_extracts.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS page_extracts (
                term TEXT NOT NULL,
                word TEXT NOT NULL,
                page_id INT NOT NULL,
                count INT DEFAULT NULL,
                excerpt TEXT DEFAULT NULL,
                is_source BIT NOT NULL,
                CONSTRAINT term_word_page_unique UNIQUE (term, word, page_id)
            );
        """
    )
    create_indexes()


def create_indexes():
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS page_word_index ON page_extracts (page_id, word);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_index ON page_extracts (term);
        """
    )


def insert_term_page(term, word, page_id, is_source=False):
    cur.execute("INSERT OR IGNORE INTO page_extracts (term, word, page_id, is_source) VALUES (?, ?, ?, ?)", [term, word, page_id, is_source])


def update_count_excerpt(word, page_id, count, excerpt):
    cur.execute("UPDATE page_extracts SET count=?, excerpt=? WHERE word=? AND page_id=?;", [count, excerpt, word, page_id])


def insert_term_page_count_excerpt(term, word, page_id, count, excerpt, is_source):
    cur.execute("SELECT * FROM page_extracts WHERE term=? AND word=? AND page_id=?;", [term, word, page_id])
    if cur.fetchone() is not None:
        cur.execute("UPDATE page_extracts SET count=?, excerpt=? WHERE word=? AND page_id=?", [count, excerpt, word, page_id])
        return
    cur.execute("INSERT INTO page_extracts (term, word, page_id, count, excerpt, is_source) VALUES (?, ?, ?, ?, ?, ?);", [term, word, page_id, count, excerpt, is_source])


def commit():
    con.commit()


def count_target_pages():
    cur.execute("SELECT COUNT(DISTINCT page_id) FROM page_extracts")
    return cur.fetchone()[0]


def get_page_ids():
    cur.execute("SELECT DISTINCT page_id FROM page_extracts")
    page_ids = set()
    for row in cur.fetchall():
        page_ids.add(row[0])
    return page_ids


def get_term_pages(term):
    cur.execute("SELECT DISTINCT(page_id) FROM page_extracts WHERE term=?", [term])
    return list(map(lambda x:x[0], cur.fetchall()))


def get_empty_entries():
    cur.execute("SELECT word, page_id FROM page_extracts WHERE count IS NULL OR excerpt IS NULL")
    return cur.fetchall()


def count_empty_entries():
    cur.execute("SELECT COUNT(*) FROM page_extracts WHERE count IS NULL OR excerpt IS NULL")
    return cur.fetchone()[0]


def count_entries():
    cur.execute("SELECT COUNT(*) FROM page_extracts")
    return cur.fetchone()[0]


def get_extract(word, page_id):
    cur.execute("SELECT count, excerpt FROM page_extracts WHERE word=? AND page_id=?", [word, page_id])
    row = cur.fetchone()
    if row is None:
        return None, None
    return row[0], row[1]


def get_term_page_counts(term, is_source):
    cur.execute("SELECT word, page_id, count FROM page_extracts WHERE is_source=? AND term=?", [is_source, term])
    return cur.fetchall()


def clear_count_excerpt():
    cur.execute("UPDATE page_extracts SET count=NULL, excerpt=NULL;")
    con.commit()
    cur.execute("VACUUM")
    con.commit()


def clear():
    cur.execute("DELETE from page_extracts")
    con.commit()
    cur.execute("VACUUM")
    con.commit()


def placeholder_list(list):
    return ', '.join(['?'] * len(list))