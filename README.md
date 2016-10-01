# Cinematical Judgment 

Cinematical Judgment is a Flask-based movie recommendation platform that employs machine learning to predict how other users might rate a particular film. The Pearson Correlation Algorithm drives the underlying mechanism, by drawing the difference between two user ratings. This 'Pearson Score' is then, in turn, used to estimate how others might rate a film.

The 'Eye' serves as the app's scrutinzing force. So, find the movies you love, rate them and see if 'The Eye' concurs! If not, prepare to feel wrath in the form of a saucy beratement message! So best of luck, brave movie aficionados! May the ratings be ever in your favor.

### Table of Contents 

1. [Technologies](#technologies)
2. [Features](#features)
3. [Installation](#installation)
4. [Deployment](#deployment) 
5. [Author](#author) 

## <a name="technologies"></a>Technologies

**Front-end:** [HTML5](http://www.w3schools.com/html/), [CSS](http://www.w3schools.com/css/), [Bootstrap](http://getbootstrap.com), [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/)

**Back-end:** [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [PostgreSQL](http://www.postgresql.org/), [SQLAlchemy](http://www.sqlalchemy.org/)

**Libraries:** [SQLAlchemy-Searchable](https://sqlalchemy-searchable.readthedocs.io)

**Data Set:** [100k MovieLens](http://grouplens.org/datasets/movielens/100k/)

## <a name="features"></a>Features
###Landing page:
<img align="center" src="/static/images/landing.jpg" width="500">

+ Users can register for an account. 
+ Users can log in if they already have an existing account. 
+ The user's information is saved to the session once the user is logged in. Using SQLAlchemy to query the Postgres database, the user object is returned which is then used to access user information.

###Movie Profile 
<img align="center" src="/static/images/movie_profile.jpg" width="500">

+ Users can read over movie statistics, including access to the IMDB link
+ Logged in users can submit a new rating or change an existing rating. 

###User Profile 
<img align="center" src="/static/images/user_profile.jpg" width="500">

+ All ratings submitted by user are queried
+ Users can then directly access the movie they rated to change the rating 

## <a name="installation"></a>Installation
As Cinematical Judgment has not yet been deployed, please follow these instructions to run Cinematical Judgment locally on your machine:

### Prerequisite: 

Install [PostgreSQL](http://postgresapp.com) (Mac OSX).

Postgres needs to be running in order for the app to work. It is running when you see the elephant icon:

Add /bin directory to your path to use PostgreSQL commands and install the Python library.

Use Sublime to edit `~/.bash_profile` or `~/.profile`, and add:

```export PATH=/Applications/Postgres.app/Contents/Versions/9.5/bin/:$PATH``` 

### Set up Cinematical Judgment

Clone this repository:

```$ git clone https://github.com/Afraysse/ratings_website.git```

Create a virtual environment and activate it:

```
$ virtualenv env
$ source env/bin/activate
```
Install the dependencies:

```$ pip install -r requirements.txt```

Run PostgreSQL (make sure elephant icon is active).

Create database with the name `ratings`.

```$ createdb ratings```

Seed the database with movies, users, and ratings:

```$ python seed.py```

Finally, to run the app, start the server:

```$ python server.py```

Go to `localhost:5000` in your browser to start using Cinematical Judgment!

## <a name="deployment"></a>Deployment
Deployment details coming very soon!

## <a name="author"></a>Author  
Annie Fraysse is a Software Engineer living in the San Francisco Bay Area. <br>
[LinkedIn](https://www.linkedin.com/in/annefraysse) | [Email](mailto:fraysse.anne@gmail.com) 

