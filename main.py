from page_downloads import page_downloader, page_downloads_database
from page_extraction import page_extracts_database, page_extracts_setup, page_extracts_job, source_page_extracts_job

#page_extracts_database.setup()
#page_extracts_setup.job()
print("Getting empty entries")
page_words = page_extracts_job.get_empty_pages()
print("Ensuring pages are downloaded")
page_downloads_database.setup()
page_downloader.download_multi(page_words.keys())