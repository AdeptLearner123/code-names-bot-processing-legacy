import database

# Mint, Olympus
disambiguation_ids = [652653, 12045479]

def get_paths(links, page_id):
    if page_id is None or page_id not in links:
        return [[]]
    
    paths = []
    for parent_id in links[page_id]:
        parent_paths = get_paths(links, parent_id)
        for parent_path in parent_paths:
            parent_path.append(page_id)
            paths.append(parent_path)
    
    return paths


def get_combined_paths(visited_forward, unvisited_forward, visited_backward, unvisited_backward):
    paths = []
    for page_id in unvisited_forward:
        if page_id in unvisited_backward:
            from_paths = get_paths(visited_forward, page_id)
            to_paths = get_paths(visited_backward, page_id)
            for from_path in from_paths:
                for to_path in to_paths:
                    new_path = list(from_path[:-1]) + list(reversed(to_path))
                    paths.append(new_path)
    return paths


def expand(visited, unvisited, directions):
    # visited: Map of explored pages to parent pages. Root is source article
    # to_expand: Set of page_ids in visited that haven't traversed their links
    # directions: Set of page_id tuples for all explored links
    links, new_directions = database.fetch_all_links(unvisited.keys())
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


def get_source_ids(page_id):
    if page_id in disambiguation_ids:
        link_ids, directions = database.fetch_all_links([page_id])
        return link_ids[page_id]
    return [page_id]


def bfs(from_id, to_id):
    directions = set()
    
    # Maps page_id to parent ids
    visited_forward = {from_id: [None]}
    unvisited_forward = {from_id: [None]}
    
    visited_backward = {to_id: [None]}
    unvisited_backward = {to_id: [None]}
    
    # Ensure that forward is expanded at least once, twice if disambiguation page, to ensure that there is a clue between
    expand(visited_forward, unvisited_forward, directions)
    if from_id in disambiguation_ids:
        expand(visited_forward, unvisited_forward, directions)

    expand(visited_backward, unvisited_backward, directions)
    if to_id in disambiguation_ids:
        expand(visited_backward, unvisited_backward, directions)

    paths = get_combined_paths(visited_forward, unvisited_forward, visited_backward, unvisited_backward)
        
    while len(paths) <= 0 and len(unvisited_forward) > 0 and len(unvisited_backward) > 0:        
        if len(unvisited_forward) < len(unvisited_backward):
            expand(visited_forward, unvisited_forward, directions)
        else:
            expand(visited_backward, unvisited_backward, directions)
        paths = get_combined_paths(visited_forward, unvisited_forward, visited_backward, unvisited_backward)

    return paths, directions


def print_paths(from_title, to_title):
    from_id = database.title_to_id(from_title)
    to_id = database.title_to_id(to_title)
    paths, directions = bfs(from_id, to_id)
    page_ids = set()
    
    for path in paths:
        for page_id in path:
            page_ids.add(page_id)
    
    id_to_title = database.get_titles(page_ids)
        
    print("Explored paths: " + str(len(paths)) + " edges: " + str(len(directions)))
    for path in paths:
        path_str = ''
        for i in range(len(path)):
            page_id = path[i]
            title = id_to_title[page_id] if page_id in id_to_title else "Unknown"
            path_str += title
            if i < len(path) - 1:
                next_id = path[i + 1]
                outgoing = (page_id, next_id) in directions
                incoming = (next_id, page_id) in directions
                if outgoing and incoming:
                    path_str += " <-> "
                elif outgoing:
                    path_str += " -> "
                elif incoming:
                    path_str += " <- "
                else:
                    path_str += " ? "
        print(path_str)