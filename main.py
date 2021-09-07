from tqdm import tqdm
from pyinflect import getAllInflections

from page_downloads import page_downloader, page_downloads_database
from page_extraction import page_extractor, page_extracts_database, page_extracts_setup, page_extracts_job, source_page_extracts_job
from scores import scores_job, scores_database
from tests import page_download_tests, wiki_tests, pagerank_tests
from utils import wiki_database
from utils.term_synonyms import SYNONYMS
from game import scrimmage
from pagerank import pagerank_job, pagerank_database

#print(getAllInflections('BEAR'))
scrimmage.play(10)

#page_extracts_job.job()
#page_extracts_setup.job()

#page_words = page_extracts_job.get_empty_pages()
#print(len(page_words))
#print(page_words[wiki_database.title_to_id('Bivalvia')])

#page_extracts_job.job()

#for term in tqdm(SYNONYMS):
#    for synonym in SYNONYMS[term]:
#        page_extracts_database.clear_word(term, synonym)

#print(page_extracts_database.get_extract('BEAR', wiki_database.title_to_id('Maryland')))

#print(page_extractor.count_terms('Maryland', 'BEAR', page_downloads_database.get_content(wiki_database.title_to_id('Maryland'))))

#print(page_downloads_database.get_content(202240))
#print(wiki_database.title_to_id('Bivalvia'))
#scrimmage.play(1)

#scores_database.setup()
#scores_job.output_scores_job()

#pagerank_tests.test_pagerank_scores()

#pagerank_database.setup()
#pagerank_job.job()

#scrimmage.play(1)

#print("POSITIVE")
#positive = ['Bivalvia', 'Narrative', 'Chimera_(mythology)', 'Chimera_(genetics)', 'Triceratops', 'Russia', 'Narrative', 'Earth', 'Banknote', 'Reggae', 'Bar', 'Day', 'Belt_(clothing)']
#wiki_tests.print_incoming_links(positive)

#print("NEGATIVE")
#negative = ['Chimera_(Russian_band)', 'STS-132', 'Atmosphere_(music_group)', 'Pinhead_(Hellraiser)', 'Electrolite', 'DNA_(BTS_song)', 'Bilbao']
#wiki_tests.print_incoming_links(negative)