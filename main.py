import time
import sqlite3
import random

from nltk.corpus.reader.wordnet import ADJ, ADV

from page_extraction import page_extracts_setup
from page_extraction import page_extracts_database
from page_extraction import page_extracts_job
from page_extraction import source_page_extracts_setup
from page_extraction import page_extractor
from page_downloads import page_downloads_database
from citations import citations
from citations import citations_job
from scores import scores_job
from scores import scores_database
from utils import title_utils
from utils import wiki_database
from utils.term_pages import TERM_PAGES
from game import scrimmage
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import progressbar

#print(page_extracts_database.get_extract("BEACH", "Bois-de-l\'Île-Bizard_Nature_Park"))
print(page_extracts_database.get_extract("NATURE", "Rock"))

#scrimmage.play(10)

"""
term = "ORGAN"
for row in scores_database.get_top_clues(term, 50):
    clue, score, path = row
    old_path = path
    path = path.replace('<->', '|')
    path = path.replace('<-', '|')
    path = path.replace('->', '|')
    source_title = path.split('|')[0]
    end_title = path.split('|')[-1]
    source_count, source_extract = page_extracts_database.get_extract(clue, source_title)
    target_count = 0
    if len(path.split('|')) > 1:
        target_count, target_extract = page_extracts_database.get_extract(term, end_title)
    print("{0}: {1} {2} {3} {4}".format(clue, score, old_path, source_count, target_count))
"""

#scores_database.clear()
#scores_job.output_scores_job()
#print(page_extracts_database.get_extract("EUROPE", "History"))