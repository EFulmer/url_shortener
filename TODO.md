TODO List
=========

Bugs
----
* Detect duplicate URLs better; if someone submits each of www.google.com, google.com, google.com/, http://www.google.com, that should only be one new entry in the database.

Usability
---------
* Improve the stylesheet and visual presentation, rather than just cribbing from the Flask tutorial.
* Maybe come up with a way to use "better" shortened URLs; i.e. not just ericsurlshortneer.com/1?
* Make a separate confirmation page after a URL is entered, send user to it after they actually submit the form.
* Some form of admin page that lists the short redirects and their redirect count.
    * User accounts: log in to see the redirects you submitted and the number of times they were used.

Code Cleanliness and Quality
----------------------------
* Tests. For everything.
* Clean up `tlds.py`.
    * Update tld list on startup of the app, if it's older than say, a day?
* Docstrings for all my functions.
