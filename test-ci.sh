#!/bin/bash


env=$1
fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run client and server-side tests
dev() {
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
}

# run appropriate tests
if [[ "${env}" == "development" ]]; then
  echo "Running client and server-side tests!"
  dev
fi

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi
