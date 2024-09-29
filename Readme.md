## Required steps to run the application

• Install docker and docker compose and angular cli, Node.js

• clone repository from https://github.com/hrishi7/pathfndr_assignment

• Move to the cloned folder where you can see two sub folders named flight-checker and backend

## Run the following commands inside the backend folder:

`docker-compose -f docker-compose.yaml down` (to stop containers)

`docker-compose -f docker-compose.yaml build` (to build container with multiple services like redis, flask app)

`docker-compose -f docker-compose.yaml up` (to start containers)

• Check the logs of the flask app and redis running

• Open a new terminal and move to folder flight-checker

## Run the following commands in flight-checker folder:

`npm install` (to install dependencies)

`npm run start` (to start the angular application)

## Note:

Angular application runs on port 4200(access on http://localhost:4200)

Flask rest api runs on port 1025

Rest Api documentation is available at http://localhost:1025/

Redis runs on port 6379

• If you change the flask app port, remember to update it in the angular app as well