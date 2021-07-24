import sqlite3

con = sqlite3.connect('sdow.sqlite')
cur = con.cursor()

# Ignore common articles that appear as references
ignore_ids = [
    1491462, # Library of Congress Number
    14919, # ISBN
    23538754, # Wayback Machine
    883885, # OCLC
    373399 # National diet library
]

def title_to_id(title):
    cur.execute("SELECT id FROM pages WHERE title='{0}';".format(title))
    row = cur.fetchone()
    return int(row[0])


def get_titles(page_ids):
    # Returns a map of page_id -> page_title
    id_to_title = {}
    page_ids = str(tuple(page_ids)).replace(',)', ')')
    cur.execute("SELECT id, title FROM pages WHERE id IN {0};".format(page_ids))
    rows = cur.fetchall()
    for row in rows:
        id_to_title[row[0]] = row[1]
    return id_to_title


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
