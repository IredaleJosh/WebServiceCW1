## Overview of the API

This API allows users to view movies for their runtime, revenue, genre, director and summary as well as rate them by giving a score from 1-5 and a short text review. Users can also search for certain movies, sort them by highets and lowest ranked movies or recent and latest movies. They can also search by genere too. Can login as admins to create, update and delete movies and view users details and review counts for each user. Users must authorise to either perform admin actions if they are admins or to make ratings and change their email or password.

## How to Install Dependencies?
1. Create a virtual environemnt and activate it
    python -m venv venv
    source venv/bin/activate
2. install dependencies using "pip install -r requirements.txt"

## Database setup
Project used PostgreSQL as the database backend

psql will ask for username, password and port
username can be kept as default "postgres" and the port as "5432"
password can be whatever, but keep track of it

in the database.py file, their will be at 
    database_url = "postgresql://username:password@localhost/moviedb"

username can be "postgres" and the password whatever you setup before

To create the database we do
1. Run psql with "sudo -i -u postgres" to be the postgres user
2. Enter psql with "psql"
3. Create the database with "CREATE DATABASE moviedb;"
4. Can connect to database with \c moviedb

This makes the database on psql side

we then run the import.py script with "python import.py"
We can verify the database is filled with:
    SELECT * FROM "Users";
    SELECT * FROM "Movies";

This shows the admin and the movies

## Run project

FastAPI was used
run "fastapi dev" in the terminal, ensuring app. are placed in the "__init__.py" and "models.py" files like
    app.database and app.model for __init__
    app.database for models

terminal will show links to the docs and the website

## Register and Authotising

No Users exists apart from an admin account, so new users must be registered using the "/register" endpoint
This shows the id, username and email

Once registered, you must then login using the username and password to generate a token

Go to top of the SwaggerUI and authorise by typing in:
    username, password, id of the username and the token generated

The admin account can be used to login, and perform admin actions like make movies or view user review counts

## API Documentation
APIdocumentation.pdf details the endpoints and the response models for the API 
