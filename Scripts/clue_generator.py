import breadth_first_search as search
import database
import wiki_downloader
import progressbar

def get_link_scores(from_id, to_id):
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
        title = id_to_title[page_id] if page_id in id_to_title else "Unknown"
        to_score = to_scores[page_id]
        from_score = from_scores[page_id]
        score = to_score * from_score
        score /= (title.count('_') + 1)
        combined_scores.append((title, score, from_score, to_score))
        
        if score > max_score:
            max_score = score
    
    combined_scores.sort(key = lambda tup:tup[1], reverse=True)
    return combined_scores


def get_word_scores(clue_options, from_title, to_title):
    word_scores = []
    bar = progressbar.ProgressBar(maxval=len(clue_options), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(len(clue_options)):
        bar.update(i + 1)
        clue_option = clue_options[i]
        counts = wiki_downloader.count_words(clue_option, [from_title, to_title])
        from_count = counts[from_title.lower()]
        to_count = counts[to_title.lower()]
        word_score = from_count * to_count
        word_scores.append((clue_option, word_score, from_count, to_count))
    bar.finish()
    word_scores.sort(key = lambda tup:tup[1], reverse=True)
    return word_scores


def get_clue(from_title, to_title):
    from_id = database.title_to_id(from_title)
    to_id = database.title_to_id(to_title)
    link_scores = get_link_scores(from_id, to_id)

    # Ignore invalid clues
    link_scores = list(filter(lambda tup: is_valid_clue(tup[0], from_title, to_title), link_scores))
    # Only keep top link scores
    max_link_score = link_scores[0][1]
    link_scores = list(filter(lambda tup: tup[1] == max_link_score, link_scores))

    clue_options = list(map(lambda tup: tup[0], link_scores))
    word_scores = get_word_scores(clue_options, from_title, to_title)
    return word_scores[0][0], word_scores


def is_valid_clue(title, from_title, to_title):
    from_word = from_title.lower()
    to_word = to_title.lower()
    for word in title.split("_"):
        word = word.lower()
        if word == from_word or word == to_word:
            return False
    return True


def print_clue_output(from_title, to_title):
    clue, scores = get_clue(from_title, to_title)
    print("Best clue: " + clue.upper())
    for score in scores:
        print(score[0] + ": " + str(score[1]))