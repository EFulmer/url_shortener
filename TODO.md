TODO List
=========

Bugs
----
* Basic URL checking; get the TLD and check it against a set of them?
* URL database should only be created if it does not already exist.
* Detect duplicate URLs better; if someone submits each of www.google.com, google.com, google.com/, http://www.google.com, that should only be one new entry in the database.

Usability
---------
* Maybe come up with a way to use "better" shortened URLs; i.e. not just ericsurlshortneer.com/1?
* Actual stylesheets.
* Make a separate confirmation page after a URL is entered, send user to it after they actually submit the form.
* Some form of admin page that lists the short redirects and their redirect count.

Code Cleanliness and Quality
----------------------------
* Clean up `tlds.py`.
** Update tld list on startup of the app, if it's older than say, a day?
* Rename `src` to `url_shortener`?
* Docstrings for all my functions.
* Testing suite!
