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
        "<User id={}>".format(user.user_id)

    def similarity(self, other):
        """ Return pearson rating for user compared to other user."""

        u_ratings = {}
        paired_ratings = {} 

        for r in self.ratings:
            u_ratings[r.movie_id] = r 

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r is not None:
                paired_ratings.append( (u_r.score, r.score) )

        if paired_ratings:
            return pearson(paired_ratings)

        else:
            return 0.0

    def predict_rating(self, movie):
        """ Predicts user's movie rating."""

        other_ratings = movie.ratings

        similarities = [
            (self.similarity(r.user), r)
            for r in other_ratings
        ]

        similarities.sort(reverse=True)

        similarities = [(sim, r) for sim, r in similarities if sim > 0]

        if not similarities:
            return None 

        numerator = sum([r.score * sim for sim, r in similarities])
        denominator = sum([sim for sim, r in similarities])

        return numerator / denominator

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    score = db.Column(db.Integer)

    # establish backref relationships
    user = db.relationship("User", backref=db.backref('user', order_by=user_id))
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
