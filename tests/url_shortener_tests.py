# this is, of course, blatantly copied from the Flask tutorial
# TODO Test cases:
# entering a "good" shortURL works properly
# entering a "bad" shortURL works properly
import os
import tempfile
import unittest

import url_shortener

class URLShortenerTestCase(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary url shortener app, and a temporary 
        database to use it.
        """
        # tempfile.mkstemp() returns a tuple containing a file 
        # descriptor and the path to the file, so we're using the file 
        # as our test-app's database here.
        self.db_fd, url_shortener.app.config['DATABASE'] = tempfile.mkstemp()
        url_shortener.app.config['TESTING'] = True
        # special method to create a test client, used so we can see 
        # exceptions thrown by the app.
        self.app = url_shortener.app.test_client()
        url_shortener.init_db()

    def tearDown(self):
        """Delete the temporary database used by the testing app."""
        # close the file, then delete it:
        os.close(self.db_fd)
        os.unlink(url_shortener.app.config['DATABASE'])

    def submit_url(self, url):
        """Helper method: send a URL to the server for shortening."""
        return self.app.post('/add', data={'url': url}, 
                             follow_redirects=True)
    def test_bad_url(self):
        """Test that a bad url returns an error message."""
        rv = self.submit_url('50 cent')
        assert "Sorry, but {0} isn't a valid URL.".format('50 cent') in rv.data


if __name__ == '__main__':
    unittest.main()

