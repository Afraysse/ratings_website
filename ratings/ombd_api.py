import requests 
from model import Movies, db

# using OMDB API for movie db
# t at the end signifies search param for title 
OMDB_URL = "http://www.omdbapi.com/?t="

def get_movie_info():
    """ Grab info from OMDB for all movies and update in db."""

    # query for all movies 
    movies = db.session.query(Movies).all()

    # iterate through the movie list
    for movie in movies:

        response = requests.get(OMDB_URL + movie.movie_title)

        # jsonify what is grabbed from the url + movie title
        json_response = response.json()

        movie.description = json_response.get('Plot', "")
        movie.genre = json_response.get('Genre', "")
        movie.image_url = json_response.get('Poster', "")
        movie.rate = json_response.get('Rated', "")

        db.session.commit()

if __name__ == "__main__":
    from server import app 
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
