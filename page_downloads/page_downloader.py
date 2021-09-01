from socket import timeout
from urllib.request import urlopen
import json
from urllib import parse
import progressbar
import time
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from page_downloads import page_downloads_database


URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='
SIMPLE_URL_PREFIX = 'https://simple.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='


def download_multi(target_titles, size = None, is_simple=False):
    start_time = time.time()
    filtered_titles = page_downloads_database.get_not_downloaded(target_titles, is_simple)
    
    if size is not None:
        filtered_titles = list(filtered_titles)[:size]
    print("DOWNLOADING Target: {0}  Not downloaded: {1}".format(len(target_titles), len(filtered_titles)))

    bar = progressbar.ProgressBar(maxval=len(filtered_titles), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    i = 0
    for title in filtered_titles:
        text = download_text(title, is_simple)
        if text is None:
            print("Failed: {0}".format(title))
        else:
            page_downloads_database.insert_page(title, text, is_simple)
        i += 1
        bar.update(i)
    bar.finish()
    print("--- %s seconds ---" % (time.time() - start_time))


def download_multi_threaded(target_titles, size = None):
    start_time = time.time()
    filtered_titles = list(page_downloads_database.get_not_downloaded(target_titles))
    
    print("DOWNLOADING Target: {0}  Not downloaded: {1}".format(len(target_titles), len(filtered_titles)))

    if size is not None:
        filtered_titles = filtered_titles[:size]

    chunk_size = 1000
    total_failed = 0
    with tqdm(total=len(filtered_titles)) as pbar:
        for i in range(0, len(filtered_titles), chunk_size):
            target = filtered_titles[i:i + chunk_size]
            failed = [0]
            results = dict()

            with ThreadPoolExecutor(max_workers=len(target)) as ex:
                futures = [ex.submit(download_save_text, title, failed, results) for title in target]
                for future in as_completed(futures):
                    pbar.update(1)

            for title in results:
                page_downloads_database.insert_page(title, results[title])
            page_downloads_database.commit()

            total_failed += failed[0]
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Failed: {0}".format(total_failed))


def download_save_text(title, failed, results):
    text = download_text(title)
    if text is None:
        failed[0] += 1
    else:
        results[title] = text


def download_text(page_title, is_simple=False):
    formatted_title = page_title.replace('\\', '')
    url = (SIMPLE_URL_PREFIX if is_simple else URL_PREFIX) + parse.quote_plus(formatted_title)

    try:
        response = urlopen(url, timeout=10)
        data_json = json.loads(response.read())
        return list(data_json['query']['pages'].values())[0]['extract']
    except timeout:
        #print('socket timed out - URL %s', url)
        return None
    except:
        #print("Failed to download text: " + page_title + " " + url)
        #print("Unexpected error:", sys.exc_info()[0])
        return None