from socket import timeout
from urllib.request import urlopen
import json
from urllib import parse
import progressbar
import time
import sys

from page_downloads import page_downloads_database


URL_PREFIX = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='
SIMPLE_URL_PREFIX = 'https://simple.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles='


def download_multi(target_titles, is_simple=False):
    start_time = time.time()
    filtered_titles = page_downloads_database.get_not_downloaded(target_titles, is_simple)
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


def download_text(page_title, is_simple):
    formatted_title = page_title.replace('\\', '')
    url = (SIMPLE_URL_PREFIX if is_simple else URL_PREFIX) + parse.quote_plus(formatted_title)

    try:
        response = urlopen(url, timeout=10)
        data_json = json.loads(response.read())
        return list(data_json['query']['pages'].values())[0]['extract']
    except timeout:
        print('socket timed out - URL %s', url)
        return None
    except:
        print("Failed to download text: " + page_title + " " + url)
        print("Unexpected error:", sys.exc_info()[0])
        return None