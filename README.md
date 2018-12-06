# serpent-api 
[![Build Status](https://travis-ci.com/Geeked-Out-Solutions/serpent-api.svg?token=ssEewjrKCrdk2sPPqJTU&branch=master)](https://travis-ci.com/Geeked-Out-Solutions/serpent-api)

<<<<<<< HEAD
![Coverage Status](https://codecov.io/gh/Geeked-Out-Solutions/serpent-api/branch/master/services/serpenttracker/project/graph/badge.svg)


=======
>>>>>>> 06f6845e764e01d89b53c136b8a1afd1c3370901
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

## Run Tests
API:
`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py test`

Client:
`docker-compose -f docker-compose-dev.yml run client npm test`

## Run Coverage
`docker-compose -f docker-compose-dev.yml run serpentapi python manage.py cov`

## Lint Project
`docker-compose -f docker-compose-dev.yml run serpentapi flake8 project`

## Access PostgreSQL DB
`docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres`

## Database Migrations
Init - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db init`

Migrate - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db migrate`

Upgrade - `docker-compose -f docker-compose-dev.yml run serpentapi python manage.py db upgrade`


# Prod Setup
You need to have AWS creds setup in the ~/.aws/credentials file similar to below:

```
[defaults]
aws_access_key_id=Blah
aws_secret_access_key=Blah
```

More information can be found [Here] on setting up AWS credentials(https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

# Setup Docker Instance
This will build a docker host on AWS
`docker-machine create --driver amazonec2 serpenttracker-prod`

Now set it as the active host:

```
docker-machine env serpenttracker-prod
eval $(docker-machine env serpenttracker-prod)
```

# Setup ENV Variables
Now that we are in the context of the AWS docker host we need to setup a few ENV variables:

1. Setup random secret_key:

Run python - `python`
This will bring you to a interactive prompt and follow the commands below to get a random value created:

```
>>> import binascii
>>> import os
>>> binascii.hexlify(os.urandom(24))
b'0ccd512f8c3493797a23557c32db38e7d51ed74f14fa7580'
```
Take this value and set it as the secret:

`export SECRET_KEY=0ccd512f8c3493797a23557c32db38e7d51ed74f14fa7580`

2. Grab the IP for the serpenttracker-prod environment variable:

Get the docker machine ip:

`docker-machine ip serpenttracker-prod`

Use this ip in the export below replacing DOCKER_MACHINE_IP:

`export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_IP`

# Start Up Docker Container
This command will spin up our application on the docker host:

`docker-compose -f docker-compose-prod.yml up -d --build`

Now create and seed the database:

`docker-compose -f docker-compose-prod.yml run serpentapi python manage.py recreate-db`

`docker-compose -f docker-compose-prod.yml run serpentapi python manage.py seed-db`

Ensure port 80 is allowed in the AWS security group for this container via the AWS console EC2 section - Will automate this soon.

Get the IP of the machine - `docker-machine ip serpenttracker-prod`

Now visit [http://docker-machine-ip] and see application.

