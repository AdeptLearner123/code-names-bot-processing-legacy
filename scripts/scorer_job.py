import wiki_database
from term_pages import TERM_PAGES
import term_page_database
from utils import extract_clue_word
from utils import count_title_words
import scores_database
import progressbar
import time
import citation_pages

def get_link_strength_and_str(directions, id_1, id_2):
    outgoing = (id_1, id_2) in directions
    incoming = (id_2, id_1) in directions
    if incoming and outgoing:
        return 2, '<->'
    elif incoming:
        return 1, '<-'
    elif outgoing:
        return 1, '->'
    else:
        return 0, '|'


def count_links_dict(links_dict):
    total = 0
    for id in links_dict:
        total += len(links_dict[id])
    return total


def output_scores(term, id_to_title):
    print("Counting: " + term)
    paths = {}
    scores = {}

    source_titles = TERM_PAGES[term]
    source_ids = wiki_database.get_ids_set(source_titles)
    page_counts = term_page_database.get_term_page_counts(term)

    source_links, directions_1 = wiki_database.fetch_all_links(source_ids)
    incoming_links = wiki_database.fetch_incoming_links_set(source_ids)
    citations = citation_pages.get_term_citations(term)
    link_1_ids = set()

    link_1_count = count_links_dict(source_links)
    print("1st degree: " + str(link_1_count))
    bar = progressbar.ProgressBar(maxval=link_1_count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()

    for source_id in source_links:
        source_title = id_to_title[source_id]
        for link_1_id in source_links[source_id]:
            if link_1_id not in id_to_title:
                continue
            link_1_title = id_to_title[link_1_id]
            # If the only connection between term and page is a citation
            if link_1_id not in incoming_links and link_1_title in citations:
                continue
            link_1_clue = extract_clue_word(link_1_title, term)
            if link_1_clue is None:
                continue
            term_count = 0
            if link_1_title in page_counts:
                term_count = page_counts[link_1_title]
            link_strength, link_str = get_link_strength_and_str(directions_1, source_id, link_1_id)
            score = 1 - 0.5 ** ((term_count + 1) * link_strength)
            title_count = count_title_words(link_1_title)
            score /= title_count

            if link_1_clue not in scores or scores[link_1_clue] < score:
                scores[link_1_clue] = score
                paths[link_1_clue] = source_title + link_str + link_1_title
                link_1_ids.add(link_1_id)
            
            i += 1
            bar.update(i)
    bar.finish()

    link_1_links, directions_2 = wiki_database.fetch_all_links(link_1_ids)

    link_2_count = count_links_dict(link_1_links)
    print("2nd degree: " + str(link_2_count))
    bar = progressbar.ProgressBar(maxval=link_2_count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()

    for link_1_id in link_1_links:
        link_1_title = id_to_title[link_1_id]
        link_1_clue = extract_clue_word(link_1_title, term)
        for link_2_id in link_1_links[link_1_id]:
            if link_2_id not in id_to_title:
                continue
            if link_2_id in link_1_ids:
                continue
            link_2_title = id_to_title[link_2_id]
            title_count = count_title_words(link_2_title)
            if title_count > 1:
                continue
            link_2_clue = extract_clue_word(link_2_title, term)
            if link_2_clue is None:
                continue
            link_strength, link_str = get_link_strength_and_str(directions_2, link_1_id, link_2_id)
            score = scores[link_1_clue] / 10 * link_strength
            score /= title_count

            if link_2_clue not in scores or scores[link_2_clue] < score:
                scores[link_2_clue] = score
                paths[link_2_clue] = paths[link_1_clue] + link_str + link_2_title

            i += 1
            bar.update(i)
    bar.finish()

    print("Inserting: " + str(len(scores)))
    bar = progressbar.ProgressBar(maxval=len(scores), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0
    bar.start()
    for clue in scores:
        scores_database.insert_term_clue(term, clue, scores[clue], paths[clue])
        i += 1
        bar.update(i)
    scores_database.commit()
    bar.finish()


def output_scores_job():
    print("Get all id to title")
    id_to_title = wiki_database.get_all_titles_dict()
    for term in TERM_PAGES:
        output_scores(term, id_to_title)

start_time = time.time()
output_scores_job()
print("--- %s seconds ---" % (time.time() - start_time))

"""
def get_scores_term(term):
    titles = TERM_PAGES[term]
    page_ids = wiki_database.get_ids_set(titles)
    return get_scores(page_ids)

# Returns a minimum spanning tree, link scores of each node, and directions
def get_scores(page_ids):
    visited = { }
    unvisited = { }
    scores = { }

    for page_id in page_ids:
        visited[page_id] = [None]
        unvisited[page_id] = [None]

    directions = set()
    expand(visited, unvisited, directions)
    for title in unvisited:
        term_page_database

    for i in range(depth):
        print("Expanding " + str(i))
        expand(visited, unvisited, directions, scores)
    return visited, scores, directions


def expand(visited, unvisited, directions):
    links, new_directions = wiki_database.fetch_all_links(unvisited.keys())
    directions.update(new_directions)

    unvisited.clear()
    for page_id in links:
        for link_id in links[page_id]:
            if link_id in visited:
                continue
            if link_id not in unvisited:
                unvisited[link_id] = [page_id]
            else:
                unvisited[link_id].append(page_id)
    
    for page_id in unvisited:
        visited[page_id] = unvisited[page_id]


def get_paths(tree, page_id):
    if page_id is None or page_id not in tree:
        return [[]]
    
    paths = []
    for parent_id in tree[page_id]:
        parent_paths = get_paths(tree, parent_id)
        for parent_path in parent_paths:
            parent_path.append(page_id)
            paths.append(parent_path)

    return paths
"""