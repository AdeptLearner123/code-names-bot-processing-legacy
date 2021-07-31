import breadth_first_search_2 as bfs
import database
import wiki_utils
import wiki_downloader
import time
import random
import progressbar

"""
f = open("words.txt", "r")
words = f.read().splitlines()
words = list(map(lambda word: wiki_utils.code_name_to_title(word), words))

page_ids = []
title_to_id = database.get_ids(words)
for title in title_to_id:
    page_ids.append(title_to_id[title])

clue_links = database.fetch_all_links_flat(page_ids)

green = 12460
hawk = 56890

def get_links(page_id):
    links_1 = database.fetch_all_links_flat([page_id])
    links_2 = database.fetch_all_links_flat(links_1)
    links_2_filtered = links_2.intersection(clue_links)
    links = links_1.union(links_2_filtered)

    print("Links 1: " + str(len(links_1)))
    print("Links 2: " + str(len(links_2)))
    print("Clue links: " + str(len(clue_links)))
    print("Filtered links 2: " + str(len(links_2_filtered)))
    print("Total: " + str(len(links)))
    return links

green_links = get_links(green)
hawk_links = get_links(hawk)
combined_links = green_links.union(hawk_links)
print("Combined links: " + str(len(combined_links)))
"""

f = open("words.txt", "r")
words = f.read().splitlines()
words = list(map(lambda word: wiki_utils.code_name_to_title(word), words))

green_links = database.fetch_all_links_flat([12460])
sample = random.sample(tuple(green_links), 100)
id_to_title = database.get_titles(green_links)

start = time.time()
bar = progressbar.ProgressBar(maxval=len(sample), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range(len(sample)):
    bar.update(i + 1)
    page_id = sample[i]
    wiki_downloader.count_words(id_to_title[page_id], words)

bar.finish()
end = time.time()
print(end - start)