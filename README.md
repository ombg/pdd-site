# PDD App

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
If you can run the following command successfully in your terminal, you should be good to go using Docker:
{{{docker-compose --version}}}