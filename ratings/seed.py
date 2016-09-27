"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
import datetime
from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users

    for row in open("seed_data/u.user"):
        row = row.rstrip()

        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id, age=age, zipcode=zipcode)

        db.session.add(user)


    db.session.commit()

def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    for row in open("seed_data/u.item"):
        row = row.rstrip()

        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

        if released_str:
            release_date = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        else:
            release_date = None

        title = title[:-7]

        movie = Movie(movie_id=movie_id,
                        title=title,
                        release_date=release_date,
                        imdb_url=imdb_url)

        db.session.add(movie)


    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        
        user_id, movie_id, score, timestamp = row.split()

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)


        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """ Sets value for next user_id after seeding db."""

    # For Max user_id in db
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # set next user_id to be max_id + 1 
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def make_eye():
    """ Add ratings eye to database. """

    eye = User(email='eye@ratings.com', password='wizard', age=None, zipcode=None)
    db.session.add(eye)
    db.session.commit()

def give_eye_ratings():
    """ supply eye with ratings. """

    eye = User.query.filter_by(email='eye@ratings.com').one()

    r1 = Rating(user_id=eye.user_id, movie_id=1, score=1)
    db.session.add(r1)

    r2 = Rating(user_id=eye.user_id, movie_id=1274, score=5)
    db.session.add(r2)

    r3 = Rating(user_id=eye.user_id, movie_id=373, score=5)
    db.session.add(r3)

    r4 = Rating(user_id=eye.user_id, movie_id=314, score=5)
    db.session.add(r4)

    r5 = Rating(user_id=eye.user_id, movie_id=95, score=1)
    db.session.add(r5)

    r6 = Rating(user_id=eye.user_id, movie_id=71, score=1)
    db.session.add(r6)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # create tables if they have not been created already
    db.create_all()

    # import data 
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
    make_eye()
    give_eye_ratings()





