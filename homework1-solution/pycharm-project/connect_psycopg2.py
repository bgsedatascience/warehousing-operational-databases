# this file was the first try to connect to the db with psycopg2, now it is used to check for entries and display of tables
import psycopg2

conn = psycopg2.connect("dbname=foo user=postgres host=localhost")
cur = conn.cursor()
cur.execute('SELECT * FROM order_overview;')
res = cur.fetchall()

for row in res:
    print(row)
