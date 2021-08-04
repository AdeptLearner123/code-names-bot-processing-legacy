import wiki_database
from term_pages import TERM_PAGES

def get_scores_term(term, depth):
    titles = TERM_PAGES[term]
    page_ids = wiki_database.get_ids_set(titles)
    return get_scores(page_ids, depth)


def get_scores_page(title, depth):
    id = wiki_database.title_to_id(title)
    return get_scores([title], depth)


# Returns a minimum spanning tree, link scores of each node, and directions
def get_scores(page_ids, depth):
    visited = { }
    unvisited = { }
    scores = { }

    for page_id in page_ids:
        visited[page_id] = [None]
        unvisited[page_id] = [None]
        scores[page_id] = 1

    directions = set()
    for i in range(depth):
        print("Expanding " + str(i))
        expand(visited, unvisited, directions, scores)
    return visited, scores, directions


def expand(visited, unvisited, directions, scores):
    links, new_directions = wiki_database.fetch_all_links(unvisited.keys())
    directions.update(new_directions)
    
    unvisited.clear()
    for page_id in links:
        for link_id in links[page_id]:
            if link_id in visited:
                continue
            link_score = scores[page_id] / 10
            if (page_id, link_id) in directions and (link_id, page_id) in directions:
                link_score *= 2
            if link_id not in unvisited:
                unvisited[link_id] = [page_id]
                scores[link_id] = link_score
            else:
                unvisited[link_id].append(page_id)
                scores[link_id] = max(link_score, scores[link_id])
    
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