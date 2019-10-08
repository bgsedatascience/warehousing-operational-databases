# Run the docker container with Postgres
docker stop postgres
docker rm postgres
docker run -d --name postgres -p 5432:5432 postgres
#Open Postsgres
docker run --rm -it --net host postgres psql --host 0.0.0.0 --user postgres

#Run a SQL script that creates an empty database and pipe that into Docker
cat Desktop/BGSE/term1/data_warehousing/warehousing-operational-databases/homework/create_db.sql | docker run --net host -i postgres psql --host 0.0.0.0 --user postgres

#Create a virtual environment
python3 -m venv yabra_venv 

#Activate virtual environment
source yabra_venv/bin/activate

#Install necessary packages
pip install psycopg2-binary
pip install pandas
pip install sqlalchemy

#Run a Python file that populates the database and normalizes it
python Desktop/BGSE/term1/data_warehousing/warehousing-operational-databases/homework/load_csv.py