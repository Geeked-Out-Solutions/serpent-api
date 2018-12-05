# serpent-api
Serpent Tracker api written in Flask

# Dev Setup
Ensure you have docker installed and run the following:

`docker-compose -f docker-compose-dev.yml up --build`

Setup the db:

`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py recreate-db`

Seed the db with users:

`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py seed-db`

Test it works:

[http://localhost/users](http://localhost/users)

# Run Tests
`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py test`

# Access PostgreSQL DB
`docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres`