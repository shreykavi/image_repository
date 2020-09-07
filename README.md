# image_repository

Repository for image storage

# Setup

1. Run the folling in a terminal to setup the .env

```
echo "source `which activate.sh`" >> ~/.bashrc
\$ source ~/.bashrc
```

2. Make sure postgres is installed ('image_repository')

3. Run the following to update Postgres

```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
