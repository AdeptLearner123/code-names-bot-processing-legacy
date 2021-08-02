import sqlite3

con = sqlite3.connect('term_counts.sqlite')
cur = con.cursor()

create_table_sql = """  CREATE TABLE IF NOT EXISTS term_counts (
                            page_title text NOT NULL,
                            term text NOT NULL,
                            count integer NOT NULL
                        ); """
cur.execute(create_table_sql)