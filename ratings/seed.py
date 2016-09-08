"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Rating, Movie, connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(age=age, zipcode=zipcode)

        db.session.add(user)

        # for progress
        if i % 100 == 0:
            print i 

    db.session.commit()



def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    for i, row in enumerate(open("seed_data/u.item")):
        row = row.rstrip()

        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

    if released_str:
        released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
    else:
        released_at = None

        title = title[:-7]

        movie = Movie(title=title,
                        released_at=released_at,
                        imdb_url=imdb_url)

        db.session.add(movie)

        if i % 100 == 0:
            print i 

    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

        if i % 1000 == 0:
            print i 

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
    """ Generate user judgemental eye."""

    eye = User(email="the-eye@of-judgment.com", password="evil")
    db.session.add(eye)
    db.session.commmit()

def eye_ratings():
    """ Build eye ratings."""

    eye = User.query.filter_by(email="the-eye@of-judgment.com").one()

    # store eye ratings for beratment messages 

        # Toy Story
    r = Rating(user_id=eye.user_id, movie_id=1, score=1)
    db.session.add(r)

    # Robocop 3
    r = Rating(user_id=eye.user_id, movie_id=1274, score=5)
    db.session.add(r)

    # Judge Dredd
    r = Rating(user_id=eye.user_id, movie_id=373, score=5)
    db.session.add(r)

    # 3 Ninjas
    r = Rating(user_id=eye.user_id, movie_id=314, score=5)
    db.session.add(r)

    # Aladdin
    r = Rating(user_id=eye.user_id, movie_id=95, score=1)
    db.session.add(r)

    # The Lion King
    r = Rating(user_id=eye.user_id, movie_id=71, score=1)
    db.session.add(r)

    db.session.commit()

########################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
