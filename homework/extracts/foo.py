import psycopg2

#this is how we connect to tbe database
#3 things in connect are host, user, and database
conn = psycopg2.connect("dbname=foo user=postgres host=localhost")

#define a cursor to work with
#cursors are the commands. the way you communcicate with the database
#cursors are created off of your connection. 
cur = conn.cursor()

#there are client-side cursors and server-side cursors
#client-side cursors, the client will allocate memory for the entire query
#server-side cursor. creates it but doesn't do anything with it 


#Now that we have the cursor defined we can execute a query. 
cur.execute('SELECT * FROM bar;')
cur.execute('INSERT INTO bar (id, name) VALUES (12, 'Shirley', 'a', 'bb');')


#When you have executed your query you need to have a list [variable?] to put your results in. 
res = cur.fetchall()

#Now all the results from our query are within the variable named rows. 
#Using this variable you can start processing the results. 
#To print the screen you could do the following. 
for row in res:
    print(row)
