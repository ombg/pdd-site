# PDD App [![Build Status](https://travis-ci.com/ombg/pdd-site.svg?branch=master)](https://travis-ci.com/ombg/pdd-site)

What does it do?
- It is a REST API to store PDD objects of an authenticated user into a database. 
    - The PDD objects contain certain attributes like name, or time stamp. They can also hold files, like videos which will be added to the database.
    - The PDD-object endpoint accepts a new video via the body of a POST request.
- It supports a user authentication system.

Features:
- Strong focus on test driven development and unit tests.
- Integration with Travis-CI.
- Uses Docker containers for the App and the database.

## Installation

### With Docker
Clone the repository:
```
git clone https://github.com/ombg/pdd-site.git
```
If you can run the following command successfully in your terminal, you should be good to go using Docker:
```
docker-compose --version
```
In the `Dockerfile`, we configure the docker image. We use a lightweight image for our development with Python and Django. The necessary Python modules and Linux packages are listed in this script, as well as the commands for setting up volumes and user configurations.
In the root directory of the cloned repository (normally `pdd-site`), run the following to build the Docker image:
```
docker build .
```
We use a Postgres database in a second Docker image to save the data, which is received via the API. Both Docker images can be built, running the `docker-compose.yml` file with this command:
```
docker-compose build
```
### Verify Installation by running the unit tests
Before having a look at the app in the browser, it makes sense to check if all unit tests pass.
```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```
This also runs [Flake8](https://flake8.pycqa.org/en/latest/), a linting tool. If you don't want to change the code, you can shorten the above command.

## Run App for Development Purposes
The command
```
docker-compose up
```
will start the App and the database and will make the app available on your local machine.
Head to `localhost:8000` in your browser and you can access the app. **Do not use it in production. This is a development setting.** 

Here is a list of the most relevant endpoints. A common usecase would be to follow the order of the commands in this table from top to bottom. 
| Task | Endpoint | 
| ------ | ------- |
| Create user | http://localhost:8000/api/user/create/ |
| Create token for user | http://localhost:8000/api/user/token/ |
| API root | http://localhost:8000/api/pdd/ |
| Create video-object | http://localhost:8000/api/pdd/videos/ |
| Create PDD object | http://localhost:8000/api/pdd/pddobjects/pdd-list/ | 
| Add video file to existing PDD object | http://localhost:8000/api/pdd/pddobjects/1/upload-video/ |


