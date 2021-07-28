import clue_generator
import breadth_first_search as search
import database

#link_ids, directions = database.fetch_all_links([652653])
#titles = database.get_titles(link_ids[652653])
#print(titles)

#clue_generator.print_clue_output("Olympus", "Lion")
#clue_generator.print_clue_output("Mint", "Stock")
#search.print_paths("Mint", "Stock")
clue_generator.print_clue_output("Hawk", "Ruler")

"""
pairs = [
    ['Green', 'Angel'],
    ['Loch_Ness', 'Police'],
    ['Tube', 'Net'],
    ['Olympus', 'Lion'],
    ['Mint', 'Stock']
]

for pair in pairs:
    print()
    print("=====================")
    print("PAIR: " + pair[0] + " " +  pair[1])
    clue_generator.print_clue_output(pair[0], pair[1])
"""