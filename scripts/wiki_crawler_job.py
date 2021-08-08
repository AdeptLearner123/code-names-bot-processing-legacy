from term_pages import TERM_PAGES
import wiki_database
import progressbar
import term_page_database
import wiki_crawler
import time

def get_page_terms():
    page_terms = {}
    term_pages = {}
    term_double_pages = {}

    print("Getting page terms")
    bar = progressbar.ProgressBar(maxval=len(TERM_PAGES), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for term in TERM_PAGES:
        term_sources = TERM_PAGES[term]
        term_ids = wiki_database.get_ids_set(term_sources)
        outgoing_ids = wiki_database.fetch_outgoing_links_set(term_ids)
        incoming_ids = wiki_database.fetch_incoming_links_set(term_ids)
        double_link_ids = outgoing_ids.intersection(incoming_ids)
        link_ids = outgoing_ids.union(incoming_ids)
        id_to_title = wiki_database.get_titles_dict(link_ids)

        link_titles = set()
        double_link_titles = set()
        for link_id in link_ids:
            if link_id in id_to_title:
                link_titles.add(id_to_title[link_id])
                if link_id in double_link_ids:
                    double_link_titles.add(id_to_title[link_id])

        for link_title in link_titles:
            if link_title not in page_terms:
                page_terms[link_title] = set()
            page_terms[link_title].add(term)

        term_pages[term] = link_titles
        term_double_pages[term] = double_link_titles
        i += 1
        bar.update(i)
    bar.finish()
    return page_terms, term_pages, term_double_pages


def process_term(term, page_terms, term_pages, term_double_pages):
    pages = term_pages[term]
    filtered_pages = set(filter(lambda page:len(page_terms[page]) >= 2, pages))
    double_pages = term_double_pages[term]
    target_pages = filtered_pages.union(double_pages)
    filtered_target_pages = term_page_database.get_missing_pages(term, target_pages)
    
    print("Processing {0}  Links: {1}  Filtered Links: {2}  Double Links: {3}  Target Links: {4}  Filtered Target Links: {5}"\
        .format(term, len(pages), len(filtered_pages), len(double_pages), len(target_pages), len(filtered_target_pages)))

    count = len(filtered_target_pages)
    bar = progressbar.ProgressBar(maxval=count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for page in filtered_target_pages:
        term_counts, excerpts = wiki_crawler.count_terms_multi(page, page_terms[page])
        if term_counts is None:
            print("Skipping")
            continue

        for term in term_counts:
            term_page_database.insert_term_page(term, page, term_counts[term], excerpts[term])
        i += 1
        bar.update(i)
    bar.finish()


def job_all():
    job(TERM_PAGES.keys())


def job(terms):
    page_terms, term_pages, term_double_pages = get_page_terms()
    for term in terms:
        process_term(term, page_terms, term_pages, term_double_pages)


start_time = time.time()
job_all()
print("--- %s seconds ---" % (time.time() - start_time))