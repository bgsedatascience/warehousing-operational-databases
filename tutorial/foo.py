import psycopg2

conn = psycopg2.connect("dbname=foo user=postgres host=localhost")
cur = conn.cursor()
cur.execute('SELECT * FROM bar;')
res = cur.fetchall()

for row in res:
    print(row)
