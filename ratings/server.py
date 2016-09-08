"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func, update 

from model import connect_to_db, db, User, Movie, Rating


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

########################################################################

@app.template_filter()
def datetimefilter(value, format='%b %d'):
    """ Convert a datetime format for accessiblity in Jinja. """

    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

########################################################################

@app.route('/')
def index():
    """Homepage rendering."""

    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def get_register():
    """ Get registration form."""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def post_register():
    """ Get entries to registration form."""

    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect('/')


@app.route('/login', methods=['GET'])
def get_login():
    """ Get request for login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def post_login():
    """ Login for returning users."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found!")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password!")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("You've successfully logged in!")
    return redirect('/users/%s' % user.user_id)

@app.route('/logout')
def logout():
    """Log out users."""

    del session["user_id"]

    flash("Successfully logged out!", "succes")

    return redirect('/')

@app.route('/users')
def user_list():
    """ List of active users."""

    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """ User profile."""

    # query for user
    user = User.query.filter(User.user_id == user_id).one()

    # query for all ratings committed by user 
    user_movies = db.session.query(Rating.user_id,
                                    Rating.movie_id,
                                    Rating.score,
                                    Movie.title).join(Movie).filter(Rating.user_id == user_id).order_by(Movie.title).all()

    return render_template('user_profile.html', user=user, user_movies=user_movies)

@app.route('/movies')
def movie_list():
    """ like users, shows list of movies. """

    # query for movies alphabetically by title 
    movies = Movie.query.order_by('title').all() 

    return render_template("movie_list.html", movies=movies)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_profile(movie_id):
    """ Queries for Movies."""

    movie = Movie.query.get(movie_id)

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(movie_id=movie_id,
                                            user_id=user_id).first()

    else:
        user_rating = None

    # Get the average rating of movie 

    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None 

    # prediction code: only predict if the user hasn't rated it yet 

    if (not user_rating) and user_id:
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    # either use prediction or real rating

    if prediction:
        # user hasn't rated; use prediction 
        effective_rating = prediction

    elif user_rating:
        # user has rated; use user rating 
        effective_rating = user_rating.score 

    else: 
        # user hasn't scored and no prediction 
        effective_rating = None 

    # get wizard's rating, either by predicting or using real rating

    the_eye = (User.query.filter_by(email="the-eye@of-judgement.com").one())

    eye_rating = Rating.query.filter_by(user_id=the_eye.user_id, movie_id=movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)

    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)

    else:
        difference = None

    # depending on difference, choose message 

    BERATEMENT_MESSAGES = [
        "I suppose you don't have such bad taste after all.",
        "I regret every decision that I've ever made that has " +
            "brought me to listen to your opinion.",
        "Words fail me, as your taste in movies has clearly " +
            "failed you.",
        "That movie is great. For a clown to watch. Idiot.",
        "Words cannot express the awfulness of your taste."
    ]

    if difference is not None:
        beratement = BERATEMENT_MESSAGES[int(difference)]

    else:
        beratement = None 

    return render_template("movie.html", movie=movie, 
                                        user_rating=user_rating,
                                        average=avg_rating,
                                        prediction=prediction,
                                        eye_rating=eye_rating,
                                        difference=difference,
                                        beratement=beratement)

@app.route('/movies/<int:movie_id>', methods=['POST'])
def movie_profile_post():
    """ Movie profile post."""

    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id, score=score)
    if rating:
        rating.score = score
        flash("Rating updated.")

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/movies/%s" % movie_id)


#####################################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
