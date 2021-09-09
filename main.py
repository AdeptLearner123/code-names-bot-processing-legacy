from tqdm import tqdm
from pyinflect import getAllInflections
import sqlite3

from game import scrimmage
from scores import scores_job, scores_database
from page_extraction import page_extractor, source_page_extracts_job
from page_downloads import page_downloads_database
from pagerank import pagerank_database
from utils import wiki_database, title_utils

#scores_database.setup()
#scores_job.output_scores_job()
#scrimmage.play(10)

#print(page_extractor.count_terms('Berlin', 'CITY', page_downloads_database.get_content(wiki_database.title_to_id('Berlin'))))

#print(pagerank_database.get_pagerank(wiki_database.title_to_id('Sucker_(zoology)')))

#link_ids = wiki_database.fetch_incoming_links_set([wiki_database.title_to_id('Octopus')])
#for link_id in tqdm(link_ids):
#  title = wiki_database.id_to_title(link_id)
#  if title is None:
#    continue
#  words = title_utils.extract_title_words(title)
#  if len(words) == 1 and words[0].upper() == "SUCKER":
#    print(title)


title_to_id = wiki_database.get_all_titles_dict()
pageranks = pagerank_database.get_pageranks()
#titles = ['Octopus', 'Berlin', 'Bermuda', 'Electric_battery']
titles = ['Mammoth']
for title in titles:
  print()
  print(title.upper())
  word_counts, _ = source_page_extracts_job.get_source_page_counts(wiki_database.title_to_id(title), title_to_id, pageranks)
  word_counts = sorted(word_counts.items(), key=lambda item:item[1], reverse=True)[:15]
  for word, count in word_counts:
    print(word, count)