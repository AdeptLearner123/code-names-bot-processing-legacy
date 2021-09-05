from page_extraction import page_extracts_job
from page_downloads import page_downloads_database, page_downloader

def extracts_job_download_test():
    print("Getting empty entries")
    page_words = page_extracts_job.get_empty_pages()
    target_ids = page_words.keys()
    filtered_ids = list(page_downloads_database.get_not_downloaded(target_ids))
    filtered_ids = filtered_ids[:5000]
    print("Ensuring pages are downloaded")
    print(filtered_ids)
    page_downloader.download_multi(filtered_ids)