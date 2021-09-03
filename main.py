import time

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from tests import term_utils_tests
from utils import wiki_database
from page_extraction import page_links_analysis
from page_extraction import page_extracts_setup
from page_extraction import page_extracts_database
from page_extraction import page_extracts_job
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database
from scores import scores_database
from scores import scores_job
from utils import term_utils
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger() 
from utils.nlp_utils import get_ne_chunks
from game import scrimmage
from page_extraction import source_page_extracts_job

term_utils_tests.test_term_sources()
#print(page_downloader.download_text(pageid))

#page_extracts_database.setup()
#page_extracts_database.transfer()

#for title in term_utils.get_all_sources():
#    if page_downloads_database.get_content(title) is None:
#        print("No content: {0}".format(title))

#print(term_utils.get_term_sources('BAR'))
#print(page_downloads_database.get_content('Bar'))
#print(wiki_database.title_to_id('Bar'))

#source_page_extracts_job.job()

#page_extracts_database.transfer()

#page_extracts_database.clear_count_excerpt()
#page_extracts_job.job()

#title = "Triceratops"
#print(page_extractor.count_terms(title, "BELL", page_downloads_database.get_content(title)))

#page_extracts_job.job()
#scores_database.setup()
#scores_job.output_scores_job()

#scrimmage.play(10)

"""
import spacy
source_nlp = spacy.load("en_core_web_sm")
print(source_nlp.pipe_names)

nlp = spacy.blank("en")
nlp.add_pipe("tok2vec", source=source_nlp)
nlp.add_pipe("parser", source=source_nlp)
nlp.add_pipe("tagger", source=source_nlp)
print(nlp.pipe_names)

#page_extracts_job.job()

def test_ne_chunk():
    text = 'While the loan from French of the English-language word "entrepreneur" dates to 1762, the word "entrepreneurism" dates from 1902 and the term "entrepreneurship" also first appeared in 1902.'
    
    #print(get_ne_chunks(tagger.tag(word_tokenize(text))))
    
    for ent in source_nlp(text).ents:
        print(ent.text)

    #print(tagger.tag(word_tokenize(text)))
    
    #doc = nlp(text)
    #for token in doc:
    #    print(token.text, token.tag_)
    #print(doc.ents)
    #print(get_ne_chunks(pos_tag(word_tokenize(text))))
    
    #print(pos_tag(word_tokenize('While the loan from French of the English-language word "entrepreneur" dates to 1762, the word "entrepreneurism" dates from 1902 and the term "entrepreneurship" also first appeared in 1902.')))

test_ne_chunk()
"""

#doc = nlp("Angelic animals alienate Billings jumped jumping")
#for token in doc:
#    print(token.text, token.lemma_)

#titles = ['Entrepreneurship', "Triceratops", "Microsoft", "Taiwan", "Glasses"]

#for title in titles:
#    print(page_extractor.count_terms_multi(title, term_utils.get_terms(), page_downloads_database.get_content(title)))

#print(getAllInflections('watch'))

#title = "Baseball"
#print(page_extractor.count_terms(title, "STRIKE", page_downloads_database.get_content(title)))
#page_extracts_job.job()

#page_extracts_database.setup()
#page_extracts_setup.job()

#titles = page_extracts_database.get_titles()
#page_downloader.download_multi_threaded(titles)

#print(page_extracts_database.get_extract("BAND", "Octopus"))

#page_extracts_database.clear_title_count_excerpt("Triceratops")

#scores_test.test_multi()

#terms = ["BERMUDA", "BATTERY", "MAMMOTH", "BAR", "OCTOPUS"]
#terms = ["BERMUDA"]
#for term in terms:
#    print("========={0}=========".format(term))
#    noun_counts, noun_excerpts = source_page_extracts_job.get_counts(term)
#    for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#        print("{0}: {1}    {2}".format(noun, noun_counts[noun], noun_excerpts[noun]))

#noun_counts, noun_excerpts = source_page_extracts_job.get_source_page_counts("Rubber_band")
#for noun, count in sorted(noun_counts.items(), key=lambda item:item[1], reverse=True):
#    print("{0}: {1}    {2}".format(noun, noun_counts[noun], noun_excerpts[noun]))

#source_page_extracts_job.job()
#scrimmage.play(1)

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

#term_utils_tests.test_term_sources()
#print(term_utils.get_term_sources("BILL"))
#print(page_links_analysis.link_scores_histogram())


#print(get_synonyms("FALL"))

#print(len(wiki_database.fetch_incoming_links_set([wiki_database.title_to_id("Bark_(sound)")])))
#term_utils_tests.test_term_sources()
#term_utils_tests.get_unprocessed_terms()

#page_links_analysis.link_scores_histogram()

#wiki_database.setup()

#print(term_utils.get_term_sources("HIMALAYAS"))

"""
term = sys.argv[1]
print(term)

start_time = time.time()
titles = term_utils.get_term_sources(term)
print(len(titles))
for title in titles:
    page_downloader.download_text(title)
print("--- %s seconds ---" % (time.time() - start_time))
"""

"""
def verify_page_extractor():
    rows = page_extracts_database.get_non_empty_entries(50)
    expected_counts = dict()
    expected_excerpts = dict()
    for word, title, count, excerpt in rows:
        if title not in expected_counts:
            expected_counts[title] = dict()
            expected_excerpts[title] = dict()
        expected_counts[title][word] = count
        expected_excerpts[title][word] = excerpt
    
    for title in expected_counts:
        words = list(expected_counts[title].keys())
        counts, excerpts = page_extractor.count_terms_multi(title, words, page_downloads_database.get_content(title))
        
        for word in words:
            if expected_counts[title][word] != counts[word]:
                print("Count failed {0}: {1} Expected {2} Got {3}".format(title, word, expected_counts[title][word], counts[word]))
            if expected_excerpts[title][word] != excerpts[word]:
                print("Excerpt failed {0}: {1} Expected {2} Got {3}".format(title, word, expected_excerpts[title][word], excerpts[word]))
"""