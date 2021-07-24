import breadth_first_search as search
import database

def get_clue_options(from_id, to_id):
    paths, directions = search.bfs(from_id, to_id)
    path_length = len(paths[0])
    from_scores = {from_id: 1}
    to_scores = {to_id: 1}
    page_ids = set()
    for path in paths:
        for i in range(len(path)):
            page_id = path[i]
            if i > 0:
                prev_id = path[i - 1]
                outgoing = (prev_id, page_id) in directions
                incoming = (page_id, prev_id) in directions
                score = 2 if outgoing and incoming else 1
                score *= from_scores[prev_id] / 10
                if page_id not in from_scores or from_scores[page_id] < score:
                    from_scores[page_id] = score
        for i in reversed(range(len(path))):
            page_id = path[i]
            if i < path_length - 1:
                prev_id = path[i + 1]
                outgoing = (page_id, prev_id) in directions
                incoming = (prev_id, page_id) in directions
                score = 2 if outgoing and incoming else 1
                score *= to_scores[prev_id] / 10
                if page_id not in to_scores or to_scores[page_id] < score:
                    to_scores[page_id] = score
                    
        for page_id in path[1:-1]:
            page_ids.add(page_id)
    
    id_to_title = database.get_titles(page_ids)
    max_score = 0
    combined_scores = []
    for page_id in page_ids:
        title = id_to_title[page_id]
        to_score = to_scores[page_id]
        from_score = from_scores[page_id]
        score = to_score * from_score / (title.count('_') + 1)
        combined_scores.append((title, score, from_score, to_score))
        
        if score > max_score:
            max_score = score
    
    combined_scores.sort(key = lambda tup:tup[1], reverse=True)
    results = list(filter(lambda tup: tup[1] == max_score, combined_scores))
    return results


def get_clue_scores(from_title, to_title):
    from_id = database.title_to_id(from_title)
    to_id = database.title_to_id(to_title)
    return get_clue_options(from_id, to_id)


scores = get_clue_scores("Green", "Angel")

for item in scores:
    print(item)