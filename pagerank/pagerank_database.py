from page_extraction.page_extracts_database import create_indexes
import sqlite3
from tqdm import tqdm

con = sqlite3.connect('pagerank/pagerank.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS pageranks (
                page_id INT NOT NULL,
                pagerank REAL NOT NULL,
                CONSTRAINT page_unique UNIQUE (page_id)
            );
        """
    )


def clear():
    cur.execute("DELETE FROM pageranks;")
    con.commit()
    cur.execute("VACUUM")


def create_index():
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS page_index ON pageranks (page_id);
        """
    )


def delete_index():
    cur.execute("DROP INDEX IF EXISTS page_index")


def insert_pageranks(scores):
    clear()
    delete_index()
    for page_id in tqdm(scores):
        cur.execute("INSERT OR IGNORE INTO pageranks (page_id, pagerank) VALUES (?, ?)", [page_id, scores[page_id]])
    con.commit()
    create_index()


def get_pagerank(page_id):
    cur.execute("SELECT pagerank FROM pageranks WHERE page_id=?", [page_id])
    return cur.fetchone()[0]


def get_pageranks():
    scores = dict()
    cur.execute("SELECT page_id, pagerank FROM pageranks;")
    for page_id, pagerank in tqdm(cur.fetchall()):
        scores[page_id] = pagerank
    return scores