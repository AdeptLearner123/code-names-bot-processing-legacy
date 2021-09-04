import time

from page_extraction import page_extracts_database
from page_extraction import page_extractor
from page_downloads import page_downloader
from page_downloads import page_downloads_database
from tqdm import tqdm

def job():
    start_time = time.time()

    print("Getting empty entries")
    page_words = get_empty_pages()
    
    print("Ensuring pages are downloaded")
    page_downloader.download_multi(page_words.keys())

    print("Getting pages {0}".format(len(page_words)))

    with tqdm(total=len(page_words)) as pbar:
        for page_id in page_words:
            text = page_downloads_database.get_content(page_id)
            if text is None:
                continue
            counts, excerpts = page_extractor.count_terms_multi(page_id, page_words[page_id], text)
            for word in page_words[page_id]:
                page_extracts_database.update_count_excerpt(word, page_id, counts[word], excerpts[word])
            page_extracts_database.commit()
            pbar.update(1)

    print("--- %s seconds ---" % (time.time() - start_time))


def get_empty_pages():
    empty_entries = page_extracts_database.get_empty_entries()
    page_words = {}
    for word, page_id in empty_entries:
        if page_id not in page_words:
            page_words[page_id] = set()
        page_words[page_id].add(word)
    return page_words