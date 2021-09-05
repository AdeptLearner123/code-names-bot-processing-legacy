from os import sched_get_priority_max
from page_downloads import page_downloader, page_downloads_database
from page_extraction import page_extracts_database, page_extracts_setup, page_extracts_job, source_page_extracts_job
from scores import scores_job, scores_database
from tests import page_download_tests
from utils import wiki_database
from game import scrimmage

scrimmage.play(2)

#print(scores_database.get_top_clues('OCTOPUS', 50))

#scores_database.setup()
#scores_job.output_scores_job()

#print(page_extracts_database.get_extract("NINJA", wiki_database.title_to_id('Ninjago')))
#source_page_extracts_job.job()
#page_extracts_job.job()
#page_extracts_database.clear_source_entries()