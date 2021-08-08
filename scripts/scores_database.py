import sqlite3

con = sqlite3.connect('scores.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS term_clue (
                term TEXT NOT NULL,
                clue TEXT NOT NULL,
                score REAL NOT NULL,
                path TEXT NOT NULL,
                CONSTRAINT term_clue_unique UNIQUE (term, clue)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_clue_index ON term_clue (term, clue);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS term_index ON term_clue (term);
        """
    )


def insert_term_clue(term, clue, score, path):
    cur.execute("SELECT * FROM term_clue WHERE term=? AND clue=?;", [term, clue])
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO term_clue (term, clue, score, path) VALUES(?,?,?,?);", [term, clue, score, path])
    else:
        cur.execute("UPDATE term_clue SET score=?, path=? WHERE term=? AND clue=?;", [score, path, term, clue])


def commit():
    con.commit()


def get_top_clues(term, count, reverse=False):
    order_str = "ASC" if reverse else "DESC"
    cur.execute("SELECT clue, score, path FROM term_clue WHERE term=? ORDER BY score {0} LIMIT ?".format(order_str), [term, count])
    return cur.fetchall()


def get_scores(term):
    cur.execute("SELECT clue, score FROM term_clue WHERE term=?", [term])
    scores = {}
    for row in cur.fetchall():
        scores[row[0]] = row[1]
    return scores


def get_term_clue(term, clue):
    cur.execute("SELECT score, path FROM term_clue WHERE term=? AND clue=?", [term, clue])
    return cur.fetchone()