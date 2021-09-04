import sqlite3
from tqdm import tqdm

con = sqlite3.connect('utils/wiki.sqlite')
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
    253375, #HarperCollins
]


def setup():
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS link_id_index ON links (id);
        """
    )
    cur.execute(
        """
            CREATE INDEX IF NOT EXISTS title_index ON pages (title);
        """
    )


def get_indexes():
    cur.execute(
        """
            SELECT name 
            FROM sqlite_master 
            WHERE type = 'index';
        """
    )
    return cur.fetchall()


def title_exists(title):
    cur.execute("SELECT id FROM pages WHERE title=?;", [title])
    return cur.fetchone() is not None

def title_to_id(title):
    cur.execute("SELECT id FROM pages WHERE title=?;", [title])
    row = cur.fetchone()
    return int(row[0])


def id_to_title(page_id):
    cur.execute("SELECT title FROM pages WHERE id=?;", [page_id])
    row = cur.fetchone()
    return row[0]


def get_titles_set(page_ids):
    titles = set()
    query = "SELECT title FROM pages WHERE id IN ({0});".format(placeholder_list(page_ids))
    cur.execute(query, list(page_ids))
    rows = cur.fetchall()
    for row in rows:
        titles.add(row[0])
    return titles


def get_ids_set(page_titles):
    ids = set()
    query = "SELECT id FROM pages WHERE title IN ({0});".format(placeholder_list(page_titles))
    cur.execute(query, list(page_titles))
    rows = cur.fetchall()
    for row in rows:
        ids.add(row[0])
    return ids


def get_titles_dict(page_ids):
    id_to_title = {}
    query = "SELECT id, title FROM pages WHERE id IN ({0});".format(placeholder_list(page_ids))
    cur.execute(query, list(page_ids))
    rows = cur.fetchall()
    for row in rows:
        id_to_title[row[0]] = row[1]
    return id_to_title


def get_all_titles_dict():
    id_to_title = {}
    cur.execute("SELECT id, title FROM pages;")
    rows = cur.fetchall()
    with tqdm(total=len(rows)) as pbar:
        for i in range(len(rows)):
            row = rows[i]
            id_to_title[row[0]] = row[1]
            pbar.update(1)
    return id_to_title


def get_ids_dict(page_titles):
    title_to_id = {}
    query = "SELECT id, title FROM pages WHERE title IN ({0});".format(placeholder_list(page_titles))
    cur.execute(query, list(page_titles))
    rows = cur.fetchall()
    for row in rows:
        title_to_id[row[1]] = row[0]
    return title_to_id


def fetch_all_links(page_ids):
    directions = set()
    ignore_ids_set = set(ignore_ids)
    query = "SELECT id, outgoing_links, incoming_links FROM links WHERE id IN ({0});".format(placeholder_list(page_ids))
    cur.execute(query, list(page_ids))
    page_links = {}
    for row in cur.fetchall():
        page_id, outgoing_links_str, incoming_links_str = row
        page_links[page_id] = set()

        for link_id in outgoing_links_str.split('|'):
            if link_id and int(link_id) not in ignore_ids_set:
                link_id = int(link_id)
                page_links[page_id].add(link_id)
                directions.add((page_id, link_id))
        for link_id in incoming_links_str.split('|'):
            if link_id and int(link_id) not in ignore_ids_set:
                link_id = int(link_id)
                page_links[page_id].add(link_id)
                directions.add((link_id, page_id))
    return page_links, directions


def fetch_double_links(page_ids):
    query = "SELECT id, outgoing_links, incoming_links FROM links WHERE id IN ({0});".format(placeholder_list(page_ids))
    cur.execute(query, list(page_ids))
    page_links = {}
    for row in cur.fetchall():
        page_id, outgoing_links_str, incoming_links_str = row

        outgoing_links = set(filter(lambda id: id and int(id) not in ignore_ids, outgoing_links_str.split('|')))
        incoming_links = set(filter(lambda id: id and int(id) not in ignore_ids, incoming_links_str.split('|')))
        page_links[page_id] = outgoing_links.intersection(incoming_links)
    return page_links


def fetch_all_links_set(page_ids):
    return fetch_links_set(page_ids, True, True)


def fetch_incoming_links_set(page_ids):
    return fetch_links_set(page_ids, False, True)


def fetch_outgoing_links_set(page_ids):
    return fetch_links_set(page_ids, True, False)


def fetch_links_set(page_ids, outgoing, incoming):
    if outgoing and incoming:
        field_str = 'outgoing_links, incoming_links'
    elif outgoing:
        field_str = 'outgoing_links'
    elif incoming:
        field_str = 'incoming_links'

    query = "SELECT {0} FROM links WHERE id IN ({1});".format(field_str, placeholder_list(page_ids))
    cur.execute(query, list(page_ids))

    link_ids = set()
    for row in cur.fetchall():
        for field in row:
            for link_id in field.split('|'):
                if link_id and int(link_id) not in ignore_ids:
                    link_ids.add(int(link_id))
    return link_ids


def get_redirect(id):
    cur.execute("SELECT target_id FROM redirects WHERE source_id=?", [id])
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]


def get_redirected_id(id):
    redirect_id = get_redirect(id)
    if redirect_id is None:
        return id
    return redirect_id


def get_redirected_ids(ids):
    return set(map(lambda id:get_redirected_id(id), ids))


def get_redirected_title(title):
    id = title_to_id(title)
    redirect_id = get_redirect(id)
    if redirect_id is None:
        return title
    return id_to_title(redirect_id)


def get_title_ids(title):
    cur.execute("SELECT id FROM pages WHERE title=?", [title])
    return list(map(lambda x:x[0], cur.fetchall()))


def placeholder_list(list):
    return ', '.join('?' for i in list)


def get_links_row(id):
    cur.execute("SELECT * FROM links WHERE id=?", [id])
    return cur.fetchone()