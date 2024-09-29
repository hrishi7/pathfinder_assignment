• Install docker and docker compose

• Open root directory -> backend

• Run the following commands:

docker-compose -f docker-compose.yaml down (to stop containers)

docker-compose -f docker-compose.yaml build (to build container with multiple services like redis, flask app)

docker-compose -f docker-compose.yaml up (to start containers)

• Check the logs of the flask app and redis running

• Open a new terminal and move to folder flight-checker

• Run the following commands:

npm install (to install dependencies)
npm run start (to start the angular application)
• Note:

Angular application runs on port 4200
Flask app runs on port 1025
Redis runs on port 6379
• If you change the flask app port, remember to update it in the angular app as well