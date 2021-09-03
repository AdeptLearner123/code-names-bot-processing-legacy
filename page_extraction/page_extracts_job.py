import time
import random

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
    title_words = get_empty_title_words(empty_entries)

    print("Getting pages {0}".format(len(title_words)))

    #titles = ['Taxaceae', 'Heptazine', 'Scream_(Usher_song)', 'Ucassaim', 'Intelligence', 'AirCars', 'Dracohors', 'Zorbeez', 'Luminox', 'Langtree', 'Hyper-V', 'WBBM_(AM)', 'Skateboard', 'Swinstead', 'Fangataufa', 'Ñawinpukyu_(Lima)', 'Krówki', 'Green_(R.E.M._album)', 'Namayan', 'Ultraman_(character)', 'Viaduct', 'Crossopriza', 'Locofocos', 'Brianchon_(crater)', 'Eneyida', 'Bridgend', 'Schwandorf', 'Baeotherates', 'Optare', 'Sparrow_(email_client)', 'Dipoenura', 'Vikas_(rocket_engine)', 'Marteria', "Raji\\'s", 'Stealth_(dinghy)', 'Noor_(missile)', 'Vamana', 'Burgers_(album)', 'Figleaves', 'Bandırma', 'Rosaneves', 'Ariel_(DJ)', 'Uzhhorod', 'Terenah', 'Prognosis', 'Futurity_(website)', 'Kompsornis', 'Miztec_(schooner_barge)', 'Barbarians_(2020_TV_series)', 'Gordita', 'Jersey_(fabric)', 'Flint', 'Octaman', 'Participant_(company)', 'Viz_(comics)', 'Concurrence', 'Zyxomma', 'Midaeium', 'Kuehneodon', 'KBMN-LD', 'Tocopherol', 'Maglev', 'Dreamlab_(album)', 'Anqoun', 'Sprinter_(cycling)', 'WBPI-CD', 'Methoxyflurane', 'Vulnerable_(song)', '286', 'Bacharach', 'Rhampsinit', 'Tamasay', 'HotelTonight', 'Reasons_(Earth,_Wind_&_Fire_song)', 'Supergravity', 'Skopje', 'Plus_(interbank_network)', 'Overhang_(architecture)', '.fi', 'Odyssey_(Magic:_The_Gathering)', 'Lesbos', 'Suzabad', 'Tontine_(horse)', 'Galacticidae', 'Deuces_(song)', 'Rosette_(award)', 'Freestone_(masonry)', 'Radomir_(town)', 'Tower_(disambiguation)', 'Anthiro', 'Clairvoyance', 'WADB_(AM)', 'Moosonee', 'Cuicuilco', 'Dekaton_(Bithynia)', 'Splatalot!', 'Éowyn', 'Bruchsal', 'Spitz', 'Melon']
    #print(titles)
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


def get_empty_title_words(empty_entries):
    title_words = {}
    for empty_entry in empty_entries:
        word, title = empty_entry    
        if title not in title_words:
            title_words[title] = set()
        title_words[title].add(word)
    return title_words