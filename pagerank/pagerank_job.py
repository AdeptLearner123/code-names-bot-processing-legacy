from sqlite3.dbapi2 import Error
from tqdm import tqdm

from utils import wiki_database
from pagerank import pagerank_database


def job():
    print("Fetch all links")
    links = wiki_database.fetch_all_outgoing_links()

    print("Fetch current page scores")
    start = pagerank_database.get_pageranks()

    print("Page ranking")
    scores = pagerank(links, max_iter=100, start=start, step_callback=pagerank_database.insert_pageranks)


def pagerank(graph, alpha=0.85, start=None, max_iter=100, tol=1.0e-6, step_callback=None):

    if start is None:
        x = dict.fromkeys(graph.keys(), 1)
    else:
        x = start

    N = len(graph)
    dangling_nodes = [n for n in graph if len(graph[n]) == 0]
  
    i = 0
    for _ in range(max_iter):
        i += 1
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in tqdm(x):
            for nbr in graph[n]:
                x[nbr] += alpha * xlast[n] / len(graph[n])
            x[n] += danglesum / N + (1.0 - alpha)
  
        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        print("Iteration {0} error: {1}  {2}".format(i, err, err / N))

        if step_callback is not None:
            step_callback(x)

        if err < N * tol:
            return x
    return x