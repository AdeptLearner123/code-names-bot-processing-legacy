import sqlite3

con = sqlite3.connect('citations/citations.sqlite')
cur = con.cursor()


def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS citations (
                page_id INT NOT NULL,
                citations TEXT NOT NULL
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS page_id_index ON citations (page_id);
        """
    )


def insert_citations(page_id, citation_ids):
    citations_str = '|'.join(str(reference_id) for reference_id in citation_ids)
    cur.execute("SELECT * FROM citations WHERE page_id=?;", [page_id])
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO citations (page_id, citations) VALUES(?,?);", [page_id, citations_str])
    else:
        cur.execute("UPDATE citations SET citations=? WHERE page_id=?;", [citations_str, page_id])
    con.commit()


def get_citations(page_id):
    cur.execute("SELECT citations FROM citations WHERE page_id=?;", [page_id])
    row = cur.fetchone()
    if row:
        citation_ids = filter(lambda i:i, row[0].split('|'))
        return set(map(lambda i:int(i), citation_ids))
    return None


def get_page_ids():
    cur.execute("SELECT DISTINCT page_id FROM citations")
    return list(map(lambda row:row[0], cur.fetchall()))