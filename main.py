from tqdm import tqdm
from pyinflect import getAllInflections
import sqlite3

from game import scrimmage
from scores import scores_job, scores_database

#scores_database.setup()
#scores_job.output_scores_job()
scrimmage.play(10)

#con = sqlite3.connect('scores/scores.sqlite')
#cur = con.cursor()
#cur.execute("SELECT * FROM term_clue LIMIT 1")
#print(cur.fetchone())