#!/bin/sh

if [ -z "$TRAVIS_PULL_REQUEST" ] || [ "$TRAVIS_PULL_REQUEST" == "false" ]
then

  if [[ "$TRAVIS_BRANCH" == "staging" ]]; then
    export DOCKER_ENV=stage
    export REACT_APP_SERPENT_SERVICE_URL="http://serpenttracker-staging-alb-155647854.us-east-1.elb.amazonaws.com"
  elif [[ "$TRAVIS_BRANCH" == "production" ]]; then
    export DOCKER_ENV=prod
    # export REACT_APP_USERS_SERVICE_URL="http://testdriven-production-alb-1112328201.us-east-1.elb.amazonaws.com"
    # export DATABASE_URL="$AWS_RDS_URI"
    # export SECRET_KEY="$PRODUCTION_SECRET_KEY"
  fi

  if [ "$TRAVIS_BRANCH" == "staging" ] || \
     [ "$TRAVIS_BRANCH" == "production" ]
  then
    curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
    unzip awscli-bundle.zip
    ./awscli-bundle/install -b ~/bin/aws
    export PATH=~/bin:$PATH
    # add AWS_ACCOUNT_ID, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY env vars
    eval $(aws ecr get-login --region us-east-1 --no-include-email)
    export TAG=$TRAVIS_BRANCH
    export REPO=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
  fi

  if [ "$TRAVIS_BRANCH" == "staging" ] || \
     [ "$TRAVIS_BRANCH" == "production" ]
  then
    # serpentapi
    docker build $SERPENTAPI_REPO -t $SERPENTAPI:$COMMIT -f Dockerfile-prod
    docker tag $SERPENTAPI:$COMMIT $REPO/$SERPENTAPI:$TAG
    docker push $REPO/$SERPENTAPI:$TAG
    # serpentapi db
    docker build $SERPENTAPI_DB_REPO -t $SERPENTAPI_DB:$COMMIT -f Dockerfile
    docker tag $SERPENTAPI_DB:$COMMIT $REPO/$SERPENTAPI_DB:$TAG
    docker push $REPO/$SERPENTAPI_DB:$TAG
    # client
    docker build $CLIENT_REPO -t $CLIENT:$COMMIT -f Dockerfile-prod --build-arg REACT_APP_SERPENT_SERVICE_URL=$REACT_APP_SERPENT_SERVICE_URL
    docker tag $CLIENT:$COMMIT $REPO/$CLIENT:$TAG
    docker push $REPO/$CLIENT:$TAG
    # swagger
    docker build $SWAGGER_REPO -t $SWAGGER:$COMMIT -f Dockerfile-prod
    docker tag $SWAGGER:$COMMIT $REPO/$SWAGGER:$TAG
    docker push $REPO/$SWAGGER:$TAG
  fi
fi
