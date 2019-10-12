# Notes on provided tutorial file. 
# Create server container running on 5432
docker run -d --name postgres -p 5432:5432 postgres

# Create client container
docker run --rm -it --net host postgres psql --host 0.0.0.0 --user postgres

# Nandan suggests putting this into a script:
echo 'docker run --rm -it --net host postgres psql "$@"' > psql.sh
# chmod +x psql.sh
# I prefer to use octal permissions
chmod 755 psql.sh

# Python virtual environment:
python3 -m venv venv && source venv/bin/activate

# This gives error about pip, it seems that the new
# virtual containers are created with a very old
# version of pip
deactivate # To deactivate the virtual environment
# then, via [ https://stackoverflow.com/questions/51644402/i-keep-getting-a-message-to-upgrade-pip ]
venv/bin/pip install -U pip
# or pip install -U virtualenv


# source venv/bin/activate
