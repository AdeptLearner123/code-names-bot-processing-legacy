from pagerank import pagerank_job
from utils import wiki_database
from pagerank import pagerank_database

def test_pagerank():
    graph = {
        0: [2],
        1: [2],
        2: [3],
        3: []
    }

    scores = pagerank_job.pagerank(graph, tol=0.1)
    print(scores)
    print(sum(scores.values()))


def test_pagerank_scores():
    titles = ['Triceratops', 'DNA_(BTS_song)', 'Belt_(clothing)', "Pinhead_(Hellraiser)"]
    for title in titles:
        print("{0}: {1}".format(title, pagerank_database.get_pagerank(wiki_database.title_to_id(title))))