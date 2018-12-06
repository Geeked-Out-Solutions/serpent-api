#!/bin/bash

fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run unit and integration tests
docker-compose -f docker-compose-dev.yml up -d --build
docker-compose -f docker-compose-dev.yml run serpentapi python manage.py test
inspect $? serpentapi
docker-compose -f docker-compose-dev.yml run serpentapi flake8 project
inspect $? serpentapi-lint
docker-compose -f docker-compose-dev.yml run serpentapi python manage.py cov
inspect $? serpentapi-cov
docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose-dev.yml down

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi