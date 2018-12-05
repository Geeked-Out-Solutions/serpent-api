# serpent-api 
[![Build Status](https://travis-ci.com/Geeked-Out-Solutions/serpent-api.svg?token=ssEewjrKCrdk2sPPqJTU&branch=master)](https://travis-ci.com/Geeked-Out-Solutions/serpent-api)

Serpent Tracker api written in Flask db uses Postgres

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
API:
`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py test`

Client:
`docker-compose -f docker-compose-dev.yml run client npm test`

# Run Coverage
`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py cov`

# Lint Project
`docker-compose -f docker-compose-dev.yml run serpentapi flake8 project`

# Access PostgreSQL DB
`docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres`

# Database Migrations
Init - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db init`

Migrate - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db migrate`

Upgrade - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db upgrade`
