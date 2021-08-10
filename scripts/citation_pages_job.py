import wiki_database
import citations_database
from term_pages import TERM_PAGES
from bs4 import BeautifulSoup
import requests
import progressbar

URL_PREFIX = 'https://en.wikipedia.org/wiki/'
PREFIX = '/wiki/'

def download_term_references(term):
    source_titles = TERM_PAGES[term]
    references = set()
    for title in source_titles:
        references.update(download_page_references(title))
    return references


def download_page_references(title):
    url = URL_PREFIX + title
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    citations = soup.find_all('cite', {})
    references = set()
    for citation in citations:
        links = citation.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith(PREFIX):
                reference = href[len(PREFIX):]
                references.add(reference)
    return references


def save_page_references(title):
    print("Page: " + title)
    id = wiki_database.title_to_id(title)
    reference_titles = download_page_references(title)
    reference_ids = wiki_database.get_ids_set(reference_titles)
    citations_database.insert_citations(id, reference_ids)


def save_all_references():
    source_titles = set()
    for term in TERM_PAGES:
        source_titles.update(TERM_PAGES[term])
    
    page_ids = citations_database.get_page_ids()
    page_titles = wiki_database.get_titles_set(page_ids)
    target_pages = source_titles.difference(page_titles)

    print("Target pages: " + str(len(target_pages)))
    bar = progressbar.ProgressBar(maxval=len(target_pages), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for title in target_pages:
        save_page_references(title)
        i += 1
        bar.update(i)
    bar.finish()