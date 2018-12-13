Introduction
============
Welcome to the Serpent Tracker documentation.  Our system is used for tracking and managing snake records and this documentation
outlines our application.


Local Development Setup
===============================================
This section will show you how to setup your local machine for local development of the application.

Setup Prequisites
*****************
Make sure you have docker and docker-compose installed and running correctly.

Setup Steps
*****************
1. Export the variable to use localhost, this variable is used in the API and client code to manage where the application is running.::
    
    export REACT_APP_SERPENT_SERVICE_URL=http://localhost

2. Run the application with docker::
    
    docker-compose -f docker-compose-dev.yml up -d --build


Documentation for Serpent Tracker
======================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

API User Model
*****************************
.. automodule:: serpentapi.project.api.models.user
   :members:
  
API Snake Model
*****************************
.. automodule:: serpentapi.project.api.models.snake
   :members:

API Auth
*******************************
.. automodule:: serpentapi.project.api.auth
   :members:
