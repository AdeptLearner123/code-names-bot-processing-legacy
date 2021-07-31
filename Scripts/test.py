import clue_generator
import breadth_first_search as search
import database
import clue_generator_multi

#link_ids, directions = database.fetch_all_links([652653])
#titles = database.get_titles(link_ids[652653])
#print(titles)

#clue_generator.print_clue_output("Olympus", "Lion")
#clue_generator.print_clue_output("Mint", "Stock")
#search.print_paths("Mint", "Stock")
#search.print_paths("Hawk", "Ruler")
#clue_generator.print_clue_output("Hawk", "Ruler")
#search.print_paths("Face", "Apple")
#clue_generator.print_clue_output("Face", "Apple")
#search.print_paths("Dinosaur", "Spot")
#clue_generator.print_clue_output("Dinosaur", "Spot")
#search.print_paths("Whale", "Apple_(disambiguation)")
#clue_generator.print_clue_output("Whale", "Apple_(disambiguation)")

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

#print(clue_generator_multi.get_clue_options(['Pyramid', 'Center', 'Square']))
search.print_paths("Pyramid", "Symmetry")
search.print_paths("Center", "Symmetry")
search.print_paths("Square", "Symmetry")