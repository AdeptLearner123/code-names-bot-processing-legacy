import breadth_first_search_2 as bfs
import database

def get_link_scores(page_ids):
    trees = {}
    scores = {}
    directions = set()

    for page_id in page_ids:
        print("bfs page id: " + str(page_id))
        page_tree, page_scores, page_directions = bfs.bfs(page_id, 2)
        trees[page_id] = page_tree
        scores[page_id] = page_scores
        print("Updating dict")
        directions.update(page_directions)
    
    clue_options = set(scores[page_ids[0]].keys())
    print("Initial clue options " + str(len(clue_options)))
    for i in range(1, len(page_ids)):
        clue_options = clue_options.intersection(set(scores[page_ids[i]].keys()))
        print("Intersected clue options " + str(len(clue_options)))

    id_to_title = database.get_titles(clue_options)
    clue_scores = []
    for clue_option in clue_options:
        if clue_option not in id_to_title:
            continue

        clue_title = id_to_title[clue_option]
        score = 1
        score /= (clue_title.count('_') + 1)
        for page_id in page_ids:
            score *= scores[page_id][clue_option]
        clue_scores.append((clue_title, clue_option, score))
    
    clue_scores.sort(key = lambda tup:tup[2], reverse=True)
    for i in range(10):
        clue_score = clue_scores[i]
        print(clue_score[0] + ": " + str(clue_score[2]))


def get_clue_options(page_titles):
    print("Getting link scores")
    page_ids = list(database.get_ids(page_titles).values())
    print("Page_ids: " + str(page_ids))
    get_link_scores(page_ids)