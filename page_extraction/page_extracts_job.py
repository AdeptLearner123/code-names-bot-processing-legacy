import time

from page_extraction import page_extracts_database
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database
import progressbar

def job():
    start_time = time.time()

    print("Ensuring pages are downloaded")
    titles = page_extracts_database.get_titles()
    page_downloader.download_multi(titles)

    print("Getting empty entries")
    empty_entries = page_extracts_database.get_empty_entries()
    title_words = {}
    for empty_entry in empty_entries:
        word, title = empty_entry    
        if title not in title_words:
            title_words[title] = set()
        title_words[title].add(word)

    print("Getting pages {0}".format(len(title_words)))

    bar = progressbar.ProgressBar(maxval=len(title_words), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    crawl_counter = 0
    for title in title_words:
        text = page_downloads_database.get_content(title)
        if text is None:
            print("Skipping")
            continue
        counts, excerpts = page_extractor.count_terms_multi(title, title_words[title], text)
        crawl_counter += 1
        #if counts is None or excerpts is None:
        #    print("Skipping")
        #    continue
        for word in title_words[title]:
            page_extracts_database.insert_count_excerpt(word, title, counts[word], excerpts[word])
        page_extracts_database.commit()
        i += 1
        bar.update(i)
    bar.finish()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Crawled articles: {0}".format(crawl_counter))