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
                term_id INT NOT NULL,
                word TEXT NOT NULL,
                page_id INT NOT NULL,
                count INT DEFAULT NULL,
                excerpt TEXT DEFAULT NULL,
                is_source BIT NOT NULL,
                CONSTRAINT term_word_title_unique UNIQUE (term_id, word, page_id)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_page_index ON page_extracts (term_id, page_id);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS page_word_index ON page_extracts (page_id, word);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_index ON page_extracts (term_id);
        """
    )


def insert_term_page(term, word, title, is_source=False):
    cur.execute("SELECT * FROM page_extracts WHERE term=? AND word=? AND title=?;", [term, word, title])
    if cur.fetchone() is not None:
        return
    cur.execute("INSERT INTO page_extracts (term, word, title, is_source) VALUES (?, ?, ?, ?)", [term, word, title, is_source])


def commit():
    con.commit()


def insert_count_excerpt(word, title, count, excerpt):
    cur.execute("UPDATE page_extracts SET count=?, excerpt=? WHERE word=? AND title=?;", [count, excerpt, word, title])


def insert_term_page_count_excerpt(term, word, title, count, excerpt, is_source):
    cur.execute("SELECT * FROM page_extracts WHERE term=? AND word=? AND title=?;", [term, word, title])
    if cur.fetchone() is not None:
        cur.execute("UPDATE page_extracts SET count=?, excerpt=? WHERE word=? AND title=?", [count, excerpt, word, title])
        return
    cur.execute("INSERT INTO page_extracts (term, word, title, count, excerpt, is_source) VALUES (?, ?, ?, ?, ?, ?);", [term, word, title, count, excerpt, is_source])


def get_term_words(term):
    cur.execute("SELECT DISTINCT word FROM page_extracts WHERE term=?", [term])
    words = []
    for row in cur.fetchall():
        words.append(row[0])
    return words


def get_word_titles(word):
    cur.execute("SELECT DISTINCT title FROM page_extracts WHERE word=?", [word])
    return list(map(lambda x:x[0], cur.fetchall()))


def count_target_pages():
    cur.execute("SELECT COUNT(DISTINCT title) FROM page_extracts")
    return cur.fetchone()[0]


def get_titles():
    cur.execute("SELECT DISTINCT title FROM page_extracts")
    titles = set()
    for row in cur.fetchall():
        titles.add(row[0])
    return titles


def get_term_titles(term):
    cur.execute("SELECT DISTINCT(title) FROM page_extracts WHERE term=?", [term])
    return list(map(lambda x:x[0], cur.fetchall()))


def get_title_words(title):
    cur.execute("SELECT DISTINCT(word) FROM page_extracts WHERE title=?", [title])
    return list(map(lambda x:x[0], cur.fetchall()))


def get_empty_entries():
    cur.execute("SELECT word, title FROM page_extracts WHERE count IS NULL OR excerpt IS NULL")
    return cur.fetchall()

def get_non_empty_entries(limit):
    cur.execute("SELECT word, title, count, excerpt FROM page_extracts WHERE count IS NOT NULL AND excerpt IS NOT NULL LIMIT ?", [limit])
    return cur.fetchall()

def get_entries():
    cur.execute("SELECT word, title FROM page_extracts")
    return cur.fetchall()


def get_term_empty_entries(term):
    cur.execute("SELECT word, title FROM page_extracts WHERE term=? AND (count IS NULL OR excerpt IS NULL)", [term])
    return cur.fetchall()


def get_empty_titles(term):
    cur.execute("SELECT DISTINCT(title) FROM page_extracts WHERE term=? AND (count IS NULL OR excerpt IS NULL)", [term])
    return list(map(lambda x:x[0], cur.fetchall()))


def count_empty_entries():
    cur.execute("SELECT COUNT(*) FROM page_extracts WHERE count IS NULL OR excerpt IS NULL")
    return cur.fetchone()[0]


def count_entries():
    cur.execute("SELECT COUNT(*) FROM page_extracts")
    return cur.fetchone()[0]


def get_extract(word, title):
    cur.execute("SELECT count, excerpt FROM page_extracts WHERE word=? AND title=?", [word, title])
    row = cur.fetchone()
    if row is None:
        return None, None
    return row[0], row[1]


def get_excerpts_with_period():
    cur.execute("SELECT term, word, title, excerpt FROM page_extracts WHERE excerpt LIKE '%.%'")
    return cur.fetchall()


def get_term_page_counts(term):
    title_count = {}
    cur.execute("SELECT word, title, count FROM page_extracts WHERE is_source=0 AND term=?", [term])
    for row in cur.fetchall():
        word, title, count = row
        if count is None:
            continue
        if title not in title_count or title_count[title] < count:
            title_count[title] = count
    return title_count


def get_title_counts(title):
    word_count = {}
    cur.execute("SELECT word, count FROM page_extracts WHERE is_source=1 AND title=?", [title])
    for row in cur.fetchall():
        word, count = row
        if word not in word_count or count > word_count[word]:
            word_count[word] = count
    return word_count


def prune_source_words(term, words):
    query = "DELETE FROM page_extracts WHERE is_source=1 AND term=? AND word NOT IN ({0})".format(placeholder_list(words))
    cur.execute(query, [term] + list(words))
    con.commit()
    return cur.rowcount


def get_source_entries(terms):
    cur.execute("SELECT word, title FROM page_extracts WHERE term IN ({0});".format(placeholder_list(terms)), terms)
    return cur.fetchall()


def placeholder_list(list):
    return ', '.join('?' for i in list)


def get_non_source_titles():
    cur.execute("SELECT DISTINCT title FROM page_extracts;")
    return set(map(lambda x:x[0], cur.fetchall()))


def clear_source_entries():
    cur.execute("DELETE FROM page_extracts WHERE is_source=1;")
    con.commit()
    cur.execute("VACUUM")
    con.commit()


def clear_title_count_excerpt(title):
    cur.execute("UPDATE page_extracts SET count=NULL, excerpt=NULL WHERE title=?", [title])
    con.commit()


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


def clear_zero_counts():
    cur.execute("UPDATE page_extracts SET count=NULL, excerpt=NULL WHERE count=0;")
    con.commit()


def filter_term_titles(term, titles):
    query = "DELETE FROM page_extracts WHERE term=? AND title NOT IN ({0})".format(placeholder_list(titles))
    cur.execute(query, [term] + list(titles))
    con.commit()
    cur.execute("VACUUM")
    con.commit()


def transfer():
    print("Transferring")
    con2 = sqlite3.connect('page_extraction/page_extracts CURRENT.sqlite')
    cur2 = con2.cursor()
    cur2.execute("SELECT term, word, title FROM page_extracts WHERE is_source=0")
    rows = cur2.fetchall()
    print("Found ", len(rows))
    term_to_id = term_utils.get_term_to_id()
    with tqdm(total=len(rows)) as pbar:
        for term, word, title in rows:
            page_id = wiki_database.title_to_id(title)
            term_id = term_to_id[term]
            cur.execute("INSERT INTO page_extracts (term_id, word, page_id, is_source) VALUES (?, ?, ?, ?);", [term_id, word, page_id, 0])
            pbar.update(1)
        con.commit()