from tqdm import tqdm
import networkx as nx

from utils import wiki_database
from pagerank import pagerank_database
from pagerank.pagerank import pagerank

def job():
    print("Fetch all links")
    links = wiki_database.fetch_all_outgoing_links()

    print("Assembling graph")
    G = nx.Graph()
    for page_id in links:
        for link in links[page_id]:
            G.add_edge(page_id, link)

    print("Page ranking")
    scores = pagerank(G)

    print("Inserting")
    pagerank_database.insert_pageranks(scores)