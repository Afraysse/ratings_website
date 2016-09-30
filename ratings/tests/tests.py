import unittest
from unittest import TestCase
from model import db, example_data, connect_to_db 
from server import app 
import server 

class MovieTestDatabase(TestCase):

    def setUp(self): 
        """ To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True 
        # Connect to test database 
        connect_to_db(app, "postgresql:///ratings_test")

        # Create tables and add sample data 
        db.drop_all()
        db.create_all()
        example_data()
        print "settup successful"

    def tearDown(self):
        """ At the end of every test."""

        db.session.close()
        db.drop_all()

        print "tearDown successful"

    def test_login(self):
        result = self.client.post("/login",
                                    data={"email": "afraysse2@gmail.com",
                                          "password": "flowers"},
                                    follow_redirects=True)

        self.assertIn("Login SUCCESS.", result.data)

    def test_fail_login(self):
        result = self.client.post("/login",
                                    data={"email": "afraysse2@gmail.com",
                                          "password": "henry"},
                                    follow_redirects=True)

        self.assertIn("Incorrect password. Try again!", result.data)

    def test_movies(self):
        """ Test movies page."""

        result = self.client.get("/movies")
        self.assertIn("L.A. Confidential", result.data)
        print "************** test_movies_page successful **************"

    def test_movie_profile_page(self): 
        """ Test movie profile page."""

        result = self.client.get('/movies/1')
        self.assertIn("My Rating", result.data)
        print "********* test_movies_profile_page successful *********"

    def test_user_profile_page(self):
        """ Test user profile page."""

        result = self.client.get('/user/1')
        self.assertIn("Email", result.data)
        print "********* user_profile_page successful *********"

class FlaskTestsLoggedIn(TestCase):
    """ Flask tests with user logged in to session."""

    def setUp(self):
        """ To do before every test."""

        app.config['TESTING'] = True 
        app.config['SECRET_KEY'] = 'key'

        self.client = app.test_client()
        connect_to_db(app, "postgresql:///ratings_test")

        # Create tables and add sample data 
        db.drop_all()
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1 

        def test_login_page(self):
            """ Test login page. """

            result = self.client.get("/users/1")
            self.assertIn("Email", result.data)

        def test_homepage(self):
            """ Test login page."""

            result = self.client.get("/")
            self.assertIn("Profile", result.data)
            self.assertNotIn("Login", result.data)

        def user_list_page(self):
            """ Test user list page."""

            result = self.client.get("/users")
            self.assertIn("")








































