"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func, update 

from model import connect_to_db, db, User, Movies, Ratings 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.template_filter()
def datetimefilter(value, format='%b %d'):
    """ Convert a datetime format for accessiblity in Jinja. """

    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

@app.route('/')
def index():
    """Homepage."""

    user_email = session.get("logged_in_user_email", None)
    if user_email is not None:
        user = User.query.filter(User.email == user_email).one()
        return render_template("homepage.html", user=user)

@app.route('/users')
def user_list():
    """ Shows user list, which will take to each user profile. """

    users = User.query.all()

    return render_template("users.html", users=users)

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """ Each user's profile page."""

    # Each user's profile page 

    user = User.query.filter_by(User.user_id == user_id).one() 

    # Need to query to get all movies rated by user 
    # Join Ratings and Movies and filter by user_id
    # Sort through movies returned, rated by user 

    # Join + Query for Movies and Ratings
    user_movies = db.session.query(Ratings.user_id,
                                    Ratings.movie_id,
                                    Ratings.score,
                                    Movies.title).join(Movies).filter(Ratings.user_id == user_id).order_by(Movies.movie_title).all()

    # user and user_movies can now be passed into jinja 
    # can be called on its attributes to display information 
    return render_template("user_profile.html", user=user, user_movies=user_movies)

@app.route('/register-login', methods=['GET'])
def register_login():
    """ Shows login and register forms."""

    # display forms for login or register
    return render_template('register_login.html')

@app.route('/register', methods=['POST'])
def register():
    """ check if user is in db, else add user."""

    # grabs values from register form 
    signup_email = request.form.get("signup_email")
    signup_password = request.form.get("signup_password")

    # if user in system, prompt to login
    # else, add user to db and log in, redirecting to homepage 
    if db.session.query(User).filter(User.email == signup_email).first():
        flash("That email is already registered! Please log in!")
        return redirect('/register_login')

    else:
        new_user = User(email=signup_email, password=signup_password, age=None, zipcode=None)
        db.session.add(new_user)
        db.session.commit()

    session["logged_in_user_email"] = signup_email
    session["logged_in_user"] = new_user.user_id

    flash("You are now a new member and logged in!", "success")

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    """ Login for returning users."""

    # grab form values 
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")

    # check to see if email and password match in db 
    # if yes, log user in 

    if db.session.query(User).filter(User.email == login_email,
                                        User.password = login_password).first():
        flash("Login success! Welcome!", "success")

        # query for user_id to to redirect user to their profile page 
        user = User.query.filter(User.email == login_email).one()

        session["logged_in_user_email"] = login_email
        session["logged_in_user"] = user.user_id 

        # pass var through a string via string formatting 
        # pass in user_id through redirected route 
        return redirect("/users/%s" % user.user_id)

    # for incorrect credentials  
    else:
        flash("Wrong password! Please try again!", "danger")
        return redirect('/register_login')

@app.route('/logout')
def logout():
    """Log out users."""

    del session["logged_in_user_email"]
    del session["logged_in_user"]

    flash("Successfully logged out!", "succes")

    return redirect('/')

@app.route('/movies')
def movie_list():
    """ like users, shows list of movies. """

    # query for movies alphabetically by title 
    movies = Movies.query.order_by(Movie.movie_title).all() 

    return render_template("movie_list.html", movies=movies)

@app.route('/movies/<int:movie_id', methods=['GET'])
def movie_profile(movie_id):
    """ 
    Shows information for each movie. Allows logged in users to 
    add/edit rating. Else, just shows movie information.

    """
    if not session.get("logged_in_user_email"):
        flash("Please login or register to begin rating your favorite movies!", "danger")
        return redirect('/register_login')

    else:

        # query by movie id to return db movie info 
        movie = Movies.query.get(movie_id)

        user = User.query.filter(User.email == session.get("logged_in_user_email")).one()
        user_id = user.user_id

        if user_id:
            user_rating = Ratings.query.filter_by(movie_id=movie_id, user_id=user_id).first()
        else:
            user_rating = None

        # prediction code: only predicts if user has not submitted a rating 
        prediction = None 

        if (not user_rating) and user_id:
            user = User.query.get(user_id)
            if user:
                prediction = user.predict_rating(movie)

        # Use prediction or use real rating 
        if prediction:
            # user has not submitted score; use prediction 
            effective_rating = prediction

        elif user_rating:
            # user has submitted score; user score 
            effective_rating = user_rating.score

        else:
            # user has not scored and no prediction made 
            effective_rating = None 

        # for wizard's rating, either by prediction or real thing 
        wizard = User.query.filter_by(email="wizard@gmail.com").one()
        wizard_rating = Ratings.query.filter_by(user_id=wizard.user_id)

        if wizard_rating is None:
            wizard_rating = wizard.predict_rating(movie)
        else:
            wizard_rating = wizard_rating.score 

        if wizard_rating and effective_rating:
            difference = abs(wizard_rating - effective_rating)
        else:
            # no wizard rating, skip difference 
            difference = None 

        # depending on difference from wizard, a message is choosen 
        BERATEMENT_MESSAGES = [
            "I suppose you don't have such bad taste after all.",
            "I regret every decision that I've ever made that has brought me to listen to your opinion.",
            "Words fail me, as your taste in movies has clearly failed you.",
            "That movie is great. For a clown to watch. Idiot.",
            "Words cannot express the awfulness of your taste."
        ]

        if difference is not None:
            beratement = BERATEMENT_MESSAGES[int(difference)]
        else:
            beratement = None

        # tallies score of each rating (people rated score per rating)
        # returns a list of tuples for count_score

        unordered_ratings = db.session.query(Ratings.score, func.count(Ratings.score)).filter(Ratings.movie_id == movie_id).group_by(Ratings.score)
        ordered_ratings = unordered_ratings.order_by(Ratings.score)
        count_score = ordered_movies.all() 

        average_rating = db.session.query(func.avg(Ratings.score)).filter(Ratings.movie_id == movie_id).one()

        # query for all ratings for one movie 
        # join ratings and movies tables and filter by user_id 
        # sort movies alphabetically by title 

        ratings = db.session.query(Ratings.movie_id,
                                    Ratings.score,
                                    Movies.movie_title).join(Movies).filter(Ratings.movie_id == movie_id).all()

        return render_template("movie_profile.html",
                                movie=movie, user_rating=user_rating,
                                average_rating=average_rating[0],
                                count_score=count_score, prediction=prediction,
                                ratings=ratings, beratement=beratement)

@app.route('/movies/int:movie_id>/rate-movie')
def rate_movie(movie_id):
    """ User rating score for each movie."""

    user_rating = request.args.get("user_rating")

    # get user_id from login email address used
    user_email = session["logged_in_user_email"]

    user = User.query.filter(User.email == user_email).one()

    user_id = user.user_id

    # check if rating in db 
    # if user rated movie previously, update rating 
    # else, add user rating to db by movie and user id's 
    if db.session.query(Ratings.score).filter(Ratings.movie_id == movie_id, Ratings.user_id == user_id).all():
        # when updating a value, need the key-value pair in update() 
        db.session.query(Ratings).filter(Ratings.movie_id == movie_id, Ratings.user_id == user_id).update({"score": user_rating})

        db.session.commit()

        flash("You have rated this movie before, but it's now been updated to %s." % (user_rating), "warning")
        return redirect('/users/%s' % user_id)

    else:
        db.session.add(Ratings(movie_id=movie_id, user_id=user_id, score=user_rating))
        db.session.commit() 

        flash("You have rated this movie %s." % (user_rating), "info")

        return redirect('/users/%s' % user_id)

    return render_template("rate_movie.html", user_rating=user_rating)

#####################################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
