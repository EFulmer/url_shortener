# this is, of course, blatantly copied from the Flask tutorial
# TODO Test cases:
# entering a "good" shortURL works properly
# entering a "bad" shortURL works properly
import html
import os
import sys
import tempfile
import unittest

# from http://stackoverflow.com/questions/1896918
testdir = os.path.dirname(__file__)
srcdir = '../url_shortener'
sys.path.insert(0, os.path.abspath( os.path.join(testdir, srcdir) ))

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

        # need a secret key, otherwise Flask will be annoyed:
        url_shortener.app.secret_key = 'testing key'
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
        resp = str(rv.data, encoding='utf8')
        assert 'Sorry, but' in resp


if __name__ == '__main__':
    unittest.main()

