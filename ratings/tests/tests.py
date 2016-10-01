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

    def test_movie_page(self):
        """ Test login page."""

        result = self.client.get("/movies/1")
        self.assertIn("Your Rating", result.data)
        self.assertNotIn("Login", result.data)

    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("Logged out.", result.data)

class LoggedOut(TestCase):
    """ Tests for when logged out of session."""

    def setUp(self):
        """ To do before every test. """

        app.config['TESTING'] = True 
        self.client = app.test_client()

    def test_homepage(self):
        """ Test homepage."""

        result = self.client.get("/")
        self.assertIn("Login", result.data)
        self.assertNotIn("Profile", result.data)

class FlaskTests(TestCase):

    def setUp(self):
        """ To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True 

    def test_login_flask_route(self):
        """ Non-database test."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Login</h1>', result.data)

    def tearDown(self):
        print ("tearDown ran")

class MyAppIntegrationTestCase(TestCase):

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['DEBUG'] = False 

    def test_home(self):
        test_client = server.app.test_client()
        result = test_client.get('/')
        self.assertIn('<h2 id="title" style="color: #ffffff">Cinematical Judgement</h2>', result.data)

    def test_users_list(self):
        test_client = server.app.test_client()
        result = test_client.get('/users')
        self.assertIn('<h3 class="panel-title">Users</h3>', result.data)

    def test_movies_list(self):
        test_client = server.app.test_client()
        result = test_client.get('/movies')
        self.assertIn('<h2 id="movie_title">Movies</h2>', result.data)

    def test_user_profile(self):
        test_client = server.app.test_client()
        result = test_client.get('/user/1')
        self.assertIn('<h3>Ratings</h3>', result.data)

    def tearDown(self):
        print ("tearDown ran")

################################################################################

if __name__ == "__main__":
    unittest.main()
