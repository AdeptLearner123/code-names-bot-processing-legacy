import sample_board
import term_utils
import wiki_database
import wiki_term_counter
import progressbar

def output_term_counts(term):
    link_ids = get_target_pages(term)
    link_titles = wiki_database.get_titles_set(link_ids)
    print("Counting: " + term)
    print("Total: " + str(len(link_titles)))
    f = open("term_counts/" + term + ".csv", "a")
    f.write("page,count")
    bar = progressbar.ProgressBar(maxval=len(link_titles), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    link_titles = list(link_titles)
    for i in range(len(link_titles)):
        bar.update(i + 1)
        link_title = link_titles[i]
        count = wiki_term_counter.count_terms(link_title, term)
        f.write(link_title + "," + str(count) + "\n")
    bar.finish()
    f.close()



def get_target_pages(term):
    source_ids = term_utils.get_term_source_pages(term)
    print("Source pages: " + str(len(source_ids)))
    target_ids = wiki_database.fetch_links_set(source_ids)
    return target_ids


terms = ["ICE CREAM"]
for term in terms:
    output_term_counts(term)