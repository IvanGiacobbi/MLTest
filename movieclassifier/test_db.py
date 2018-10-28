import sqlite3
import os
conn=sqlite3.connect('reviews.sqlite')
c=conn.cursor()
#estraiamo tutti i dati inseriti da gennaio 2018
c.execute("SELECT * FROM review_db WHERE dateRev BETWEEN '2017-01-01 00:00:00' AND DATETIME('now')")
results=c.fetchall()
conn.close()
print(results)
