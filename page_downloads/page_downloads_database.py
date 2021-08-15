import sqlite3

con = sqlite3.connect('page_downloads/page_downloads.sqlite')
cur = con.cursor()

def setup():
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS page_downloads (
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                CONSTRAINT title_unique UNIQUE (title)
            );
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS title_index ON page_downloads (title);
        """
    )


def get_not_downloaded(target_titles):
    cur.execute("SELECT DISTINCT title FROM page_downloads")
    titles = set()
    for row in cur.fetchall():
        titles.add(row[0])
    return target_titles.difference(titles)


def insert_page(title, content):
    cur.execute("SELECT title FROM page_downloads WHERE title=?;", [title])
    if cur.fetchone() is not None:
        cur.execute("UPDATE page_downloads SET content=? WHERE title=?;", [content, title])
    cur.execute("INSERT INTO page_downloads (title, content) VALUES (?, ?);", [title, content])
    con.commit()


def get_content(title):
    cur.execute("SELECT content FROM page_downloads WHERE title=?", [title])
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