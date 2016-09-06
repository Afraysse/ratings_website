"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        "<User id={}>".format(users.user_id)

class Movies(db.Model):
    """ Movies on ratings website."""

    __tablename__ = "movie"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_title = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    url = db.Column(db.String)

    def __repr__(self):
        "<Movie id={}>".format(movie.movie_id)

class Ratings(db.Model):
    """ Ratings submitted by users."""

    __tablename__ = "rating"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    score = db.Column(db.Integer)

    # establish backref relationships
    user = db.relationship("User", backref=db.backref('users', order_by=user_id))
    movie = db.relationship("Movies", backref=db.backref('movie', order_by=movie_id))

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
