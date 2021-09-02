import time

from page_extraction import page_extracts_database
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database
from tqdm import tqdm

def job():
    start_time = time.time()

    print("Ensuring pages are downloaded")
    titles = page_extracts_database.get_titles()
    page_downloader.download_multi_threaded(titles)

    print("Getting empty entries")
    empty_entries = page_extracts_database.get_empty_entries()
    title_words = {}
    for empty_entry in empty_entries:
        word, title = empty_entry    
        if title not in title_words:
            title_words[title] = set()
        title_words[title].add(word)

    print("Getting pages {0}".format(len(title_words)))

    with tqdm(total=len(title_words)) as pbar:
        for title in title_words:
            text = page_downloads_database.get_content(title)
            if text is None:
                continue
            counts, excerpts = page_extractor.count_terms_multi(title, title_words[title], text)
            for word in title_words[title]:
                page_extracts_database.insert_count_excerpt(word, title, counts[word], excerpts[word])
            page_extracts_database.commit()
            pbar.update(1)

    print("--- %s seconds ---" % (time.time() - start_time))
