import database

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


def bfs(from_id, to_id):
    directions = set()
    
    # Maps page_id to parent ids
    visited_forward = {from_id: [None]}
    unvisited_forward = {from_id: [None]}
    
    visited_backward = {to_id: [None]}
    unvisited_backward = {to_id: [None]}
    
    paths = []
        
    while len(paths) <= 0 and len(unvisited_forward) > 0 and len(unvisited_backward) > 0:        
        if len(unvisited_forward) < len(unvisited_backward):
            print("Expanding forward")
            expand(visited_forward, unvisited_forward, directions)
        else:
            print("Expanding backward")
            expand(visited_backward, unvisited_backward, directions)
        
        for page_id in unvisited_forward:
            if page_id in unvisited_backward:
                from_paths = get_paths(visited_forward, page_id)
                to_paths = get_paths(visited_backward, page_id)
                for from_path in from_paths:
                    for to_path in to_paths:
                        new_path = list(from_path[:-1]) + list(reversed(to_path))
                        paths.append(new_path)

    return paths, directions