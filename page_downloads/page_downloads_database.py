import sqlite3

con = sqlite3.connect('page_downloads/page_downloads.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS page_downloads (
                page_id INT NOT NULL,
                content TEXT NOT NULL,
                CONSTRAINT page_unique UNIQUE (page_id)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS page_index ON page_downloads (page_id);
        """
    )


def get_not_downloaded(target_ids):
    cur.execute("SELECT DISTINCT page_id FROM page_downloads")
    existing_ids = set()
    for row in cur.fetchall():
        existing_ids.add(row[0])
    return set(target_ids).difference(existing_ids)


def insert_page(page_id, content):
    cur.execute("SELECT page_id FROM page_downloads WHERE page_id=?;", [page_id])
    if cur.fetchone() is not None:
        cur.execute("UPDATE page_downloads SET content=? WHERE page_id=?;", [content, page_id])
    cur.execute("INSERT INTO page_downloads (page_id, content) VALUES (?, ?, ?);", [page_id, content])


def commit():
    con.commit()


def get_content(page_id):
    cur.execute("SELECT content FROM page_downloads WHERE page_id=?", [page_id])
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]


def get_count():
    cur.execute("SELECT COUNT(*) FROM page_downloads")
    return cur.fetchone()[0]


def get_sample_entries(count):
    cur.execute("SELECT title, content FROM page_downloads LIMIT ?", [count])
    return cur.fetchall()


#def clear():
#    cur.execute("DELETE from page_downloads")
#    con.commit()
#    cur.execute("VACUUM")
#    con.commit()