from page_downloads import page_downloader, page_downloads_database
from page_extraction import page_extracts_database, page_extracts_setup, page_extracts_job, source_page_extracts_job
from scores import scores_job, scores_database
from tests import page_download_tests, wiki_tests, pagerank_tests
from utils import wiki_database
from game import scrimmage
from pagerank import pagerank_job, pagerank_database


#pagerank_tests.test_pagerank_scores()

#pagerank_database.setup()
pagerank_job.job()

#scrimmage.play(1)

#print("POSITIVE")
#positive = ['Bivalvia', 'Narrative', 'Chimera_(mythology)', 'Chimera_(genetics)', 'Triceratops', 'Russia', 'Narrative', 'Earth', 'Banknote', 'Reggae', 'Bar', 'Day', 'Belt_(clothing)']
#wiki_tests.print_incoming_links(positive)

#print("NEGATIVE")
#negative = ['Chimera_(Russian_band)', 'STS-132', 'Atmosphere_(music_group)', 'Pinhead_(Hellraiser)', 'Electrolite', 'DNA_(BTS_song)', 'Bilbao']
#wiki_tests.print_incoming_links(negative)