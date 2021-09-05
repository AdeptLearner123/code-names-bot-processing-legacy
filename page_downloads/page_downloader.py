from socket import timeout
import requests
from urllib.request import urlopen
import json
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from page_downloads import page_downloads_database


#WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&pageids='

def download_multi(target_ids, size = None):
    start_time = time.time()
    filtered_ids = list(page_downloads_database.get_not_downloaded(target_ids))
    
    print("DOWNLOADING Target: {0}  Not downloaded: {1}".format(len(target_ids), len(filtered_ids)))

    if size is not None:
        filtered_ids = filtered_ids[:size]

    chunk_size = 1000
    total_failed = 0
    with tqdm(total=len(filtered_ids)) as pbar:
        for i in range(0, len(filtered_ids), chunk_size):
            target = filtered_ids[i:i + chunk_size]
            failed = [0]
            results = dict()

            with ThreadPoolExecutor(max_workers=len(target)) as ex:
                futures = [ex.submit(download_save_text, page_id, failed, results) for page_id in target]
                for future in as_completed(futures):
                    pbar.update(1)

            for page_id in results:
                page_downloads_database.insert_page(page_id, results[page_id])
            page_downloads_database.commit()

            total_failed += failed[0]
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Failed: {0}".format(total_failed))


def download_save_text(page_id, failed, results):
    text = download_text(page_id)
    if text is None:
        failed[0] += 1
    else:
        results[page_id] = text


def download_text(page_id):
    #query_params = {
    #    'action': 'query',
    #    'format': 'json',
    #    'prop': 'extracts',
    #    'pageids': page_id
    #}

    try:
        url = URL_PREFIX + str(page_id)
        response = urlopen(url, timeout=10)
        response = json.loads(response.read())
        return response.get('query', {}).get('pages', {}).get(str(page_id), {}).get('extract', None)
        #response = requests.get(WIKIPEDIA_API_URL, params=query_params, timeout=6)
        #return response.json().get('query', {}).get('pages', {}).get(str(page_id), {}).get('extract', None)
    except timeout:
        return None
    except:
        return None