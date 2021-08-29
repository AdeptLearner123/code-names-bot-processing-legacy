from enum import unique
import time
import sqlite3
import random
from textblob import TextBlob
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.corpus.reader.wordnet import ADJ, ADV
import re

from page_extraction import page_extracts_setup
from page_extraction import page_extracts_database
from page_extraction import page_extracts_job
from page_extraction import source_page_extracts_setup
from page_extraction import source_page_extracts_job
from page_extraction import page_extractor
from page_extraction import page_links_analysis
from page_downloads import page_downloads_database
from citations import citations
from citations import citations_job
from scores import scores_job
from scores import scores_database
from scores import scores_test
from utils import title_utils
from utils import wiki_database
from utils.term_pages import TERM_PAGES
from utils import txt_to_js
from utils.title_utils import extract_title_words
from utils.title_utils import count_title_words
from game import scrimmage
from game import clue_generator
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
import progressbar


#print(page_extracts_database.get_extract("BUG", "Animal"))

#scores_test.test_multi()

#terms = ["BERMUDA", "BATTERY", "MAMMOTH", "BAR", "OCTOPUS"]
#terms = ["MAMMOTH"]
#for term in terms:
#    print("========={0}=========".format(term))
#    noun_counts = source_page_extracts_job.get_counts(term)
#    for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#        print("{0}: {1}".format(noun, noun_counts[noun]))

#lemmatizer = WordNetLemmatizer()
#print(lemmatizer.lemmatize("alcoholic"))

#noun_counts = source_page_extracts_job.get_counts("BAR")
#for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#   print("{0}: {1}".format(noun, noun_counts[noun]))

#noun_counts = source_page_extracts_job.get_counts("OCTOPUS")
#for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#   print("{0}: {1}".format(noun, noun_counts[noun]))

#noun_counts = source_page_extracts_job.get_source_page_counts("Bar_(establishment)")
#for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#   print("{0}: {1}".format(noun, noun_counts[noun]))

#text = TextBlob("The cat and the dog are friends.")
#print(text.noun_phrases)


# pip install -U spacy
# python -m spacy download en_core_web_sm


#chunk_counts = dict()
#doc = nlp(page_downloads_database.get_content("Bar_(establishment)"))
#for chunk in doc.noun_chunks:
#    nc = chunk.text.lower()
#    if ' ' in nc:
#        continue
#    if nc not in chunk_counts:
#        chunk_counts[nc] = 1
#    else:
#        chunk_counts[nc] += 1

#chunk_counts = source_page_extracts_job.get_counts("BERMUDA")
#for noun, count in sorted(chunk_counts.items(), key=lambda item:item[1], reverse=True):
#   print("{0}: {1}".format(noun, chunk_counts[noun]))

#page_links_analysis.link_scores_histogram()
#page_extracts_database.setup()
#page_extracts_setup.job()
#page_extracts_job.job()

#scores_database.setup()
#scores_job.output_scores_job()
#scrimmage.play(10)

#print(scores_database.get_term_clue("ORGAN", "BIVALVIA"))

#lemmatizer = WordNetLemmatizer()
#id = wiki_database.title_to_id("Electric_battery")
#link_ids = wiki_database.fetch_outgoing_links_set([id])
#titles = wiki_database.get_titles_set(link_ids)
#titles = map(lambda title:lemmatizer.lemmatize(extract_title_words(title)[-1]), titles)
#titles = set(titles)
#print(titles)

#scores_test.test_multi()
#scores_database.setup()
#scores_job.output_scores_job()


#id = wiki_database.title_to_id("Day")
#link_ids = wiki_database.fetch_all_links_set([id])
#titles = page_extracts_setup.filter_single_titles(link_ids, wiki_database.get_all_titles_dict())
#print(titles)
#page_extracts_database.filter_term_titles("DAY", titles)

#scores_database.clear()
#scores_job.output_scores_job()

#for clue, score, title in scores_database.get_top_clues("DAY", 50):
#    print("{0}: {1}   {2}".format(clue, score, title))

#print(clue_generator.best_clue(["DAY", "LION"], [], 10))
#scores_database.init("scores (filtered day)")
#print(clue_generator.best_clue(["DAY", "LION"], [], 10))

#id_to_title = wiki_database.get_all_titles_dict()
#single_titles = list(filter(lambda item:count_title_words(item[1]) == 1, id_to_title.items()))
#print(len(single_titles))

#print(pos_tag(word_tokenize("We purhcased new figher aircraft.")))

page_links_analysis.link_scores_histogram()