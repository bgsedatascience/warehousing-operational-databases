# Homework Week 1

You will find data, in 3 csv files, in the "extracts" folder. 

Your job is to create a SQL database, in Postgres, to store this data in _normalized_ form (3NF!). You will submit: 

1. A .sql file containing sql queries to create the database and tables. 
2. A .py file containing Python code to load the data from the csv's into the database. 

As the database is not updated, but just created from scratch every time, there was no need to mount a volume to it as it is fine if the volatile storage is destroyed with the container.

To start the server, run start_server.sh:
./start_server.sh

To run postgres interactively, run postgres_interactive.sh
./postgres_interactive.sh

To run the database creation SQL file and the Python insert file, run run_hw.sh
./run_hw.sh
