import sqlite3

con = sqlite3.connect('wiki.sqlite')
cur = con.cursor()

# Ignore common articles that appear as references
ignore_ids = [
    1491462, # Library of Congress Number
    14919, # ISBN
    23538754, # Wayback Machine
    883885, # OCLC
    373399, # National diet library
    35566739, # Integrated Authority File
    422994, # Digital object identifier
    9898086, # Mint (newspaper)
    48455863, # Semantic Scholar
    503009, #PubMed
]

def title_to_id(title):
    cur.execute("SELECT id FROM pages WHERE title='{0}';".format(title))
    row = cur.fetchone()
    return int(row[0])


def id_to_title(page_id):
    cur.execute("SELECT title FROM pages WHERE id='{0}';".format(page_id))
    row = cur.fetchone()
    return int(row[0])


def get_titles_set(page_ids):
    titles = set()
    page_ids = str(tuple(page_ids)).replace(',)', ')')
    cur.execute("SELECT title FROM pages WHERE id IN {0};".format(page_ids))
    rows = cur.fetchall()
    for row in rows:
        titles.add(row[0])
    return titles


def get_ids_set(page_titles):
    ids = set()
    page_titles = str(tuple(page_titles)).replace(',)', ')')
    cur.execute("SELECT id FROM pages WHERE title IN {0};".format(page_titles))
    rows = cur.fetchall()
    for row in rows:
        ids.add(row[0])
    return ids


def get_ids_dict(page_titles):
    title_to_id = {}
    page_titles = str(tuple(page_titles)).replace(',)', ')')
    cur.execute("SELECT id, title FROM pages WHERE title IN {0};".format(page_titles))
    rows = cur.fetchall()
    for row in rows:
        title_to_id[row[1]] = row[0]
    return title_to_id


def fetch_all_links(page_ids):
    # Returns map (page_id -> list of page_ids)
    directions = set()
    page_ids = str(tuple(page_ids)).replace(',)', ')')
    cur.execute("SELECT id, outgoing_links, incoming_links FROM links WHERE id IN {0};".format(page_ids))
    page_links = {}
    for row in cur.fetchall():
        page_id = row[0]
        outgoing_links_str = row[1]
        incoming_links_str = row[2]
        page_links[page_id] = set()

        for link_id in outgoing_links_str.split('|'):
            if link_id and int(link_id) not in ignore_ids:
                link_id = int(link_id)
                page_links[page_id].add(link_id)
                directions.add((page_id, link_id))
        for link_id in incoming_links_str.split('|'):
            if link_id and int(link_id) not in ignore_ids:
                link_id = int(link_id)
                page_links[page_id].add(link_id)
                directions.add((link_id, page_id))
    return page_links, directions


def fetch_links_set(page_ids):
    page_ids = str(tuple(page_ids)).replace(',)', ')')
    cur.execute("SELECT outgoing_links, incoming_links FROM links WHERE id IN {0};".format(page_ids))
    link_ids = set()
    for row in cur.fetchall():
        for link_id in row[0].split('|'):
            if link_id:
                link_ids.add(int(link_id))
        for link_id in row[1].split('|'):
            if link_id:
                link_ids.add(int(link_id))
    return link_ids