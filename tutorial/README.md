# Setting up Postgres with Docker


## Running the database

Running a postgres database is easy!

``` shell
docker run -d --name postgres -p 5432:5432 postgres
```

Note: think about what you want to happen to the data in your database. If you `rm` your container, with the above command, your data will dissapear! This may or may not be what you want, depending on what you are doing.

Optionally, you can add a volume mount to the data directory of postgres. Take a look at the postgres docker documentation to see how! Bonus: this could be a good time to make a named volume (look up "docker named volumes" to see what that gives you).

## Connecting to the database

Now you can connect to the database. To do that, we will use the `psql` command-line client. This is a simple command-line tool that allows us to connect to a postgres database and make queries.

We could install the `psql` tool locally, but it already exists in the `postgres` docker container, so we can just use that! Let's run another container as a client:

``` shell
docker run --rm -it --net host postgres psql --host 0.0.0.0 --user postgres
```

We might already be able to see that this could get tedious to write, so let's put it into a script:

``` shell
echo 'docker run --rm -it --net host postgres psql "$@"' > psql.sh
chmod +x psql.sh
```

Now we can use the script:

``` shell
./psql.sh --host 0.0.0.0 --user postgres
```

## Using the psql prompt

Once we're in the prompt, we can look around:

List databases with `\l`

One Postgres server can host multiple "databases". Each of these databases is logically separated from each other.

Connect to a database with `\c`

Describe a database with `\d`

Describe a table with `\d tablename`

But note, we're going to need to create a database and define some tables before we can do anything else!

``` sql
CREATE DATABASE foo;
\c foo;
```

Now let's create a table in our database foo:

``` sql
CREATE TABLE bar (
id INTEGER PRIMARY KEY,
name VARCHAR NOT NULL,
phone_number VARCHAR,
salary MONEY
);
```

That's it! Now we can enter some data:

``` sql
INSERT INTO bar (id, name) VALUES (234, 'Nandan');
```

And see that we entered it correctly:

``` sql
SELECT * FROM bar;
```

## Connecting from Python

We can connect to Postgres from Python!

We're not going to use Jupyter notebooks for this, we're going to create a Python script.

The first step will be to create a folder where you want to work, and install a virtual environment:

``` shell
python3 -m venv venv && source venv/bin/activate
```

Hint: this is something you will do often, so you can alias it or put it into a script to reuse!

Now we can install the drivers necessary to communicate with Postgres. The most common is called psycopg2 and we can install it with pip. First, make sure you're installing in the virtual environment you created:

``` shell
which pip
```

Then install it:

``` shell
pip install psycopg2-binary
```

Now let's create a python file and write the following:

``` python
import psycopg2

conn = psycopg2.connect("dbname=foo user=postgres host=localhost")
cur = conn.cursor()
cur.execute('SELECT * FROM bar;')
res = cur.fetchall()

for row in res:
    print(row)

```

`psycopg2` is very fast and it's the most popular Postgres connector for Python. But there are many other libraries we could use, that internally will use `psycopg2`, and many have nicer interfaces.

Here are two worth looking at:

`records`
`dataset`

I especially recommend using `dataset` for the assignment if you want to be lazy and unsafe, but avoid writing tedious sql!
