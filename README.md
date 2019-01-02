# Gratitude-Journal
https://gratitude-journal-chris.herokuapp.com/

Feel free to clone this app onto your own machine if you would like to run the test suite (`python manage.py test` in the directory containing the manage.py file.)  Know that you will need the [chrome web driver](http://chromedriver.chromium.org/downloads) for selenium to function properly so the tests will run.  You may need to change the path to the web driver in the Gratitude Journal/tests.py file.

This is a site where users can post gratitude journals, either publicly, for others to see, or privately, for their own eyes only.  They can explore other user's public journals, and if they so choose they can follow a given user, whose public journals will appear in reverse chronological order in their feed.  Users can follow an unlimited number of other users.  Users can also upload one profile picture, which will appear on their profile and next to their own journals.  I will explain the various pages of the site below:

## Index

Has a form for users to submit a new journal, as well as a spot to review their last few journals.  Inaccessible to unauthenticated users.  

## Explore

The landing page for unauthenticated users.  If a user is unauthenticated this page will have buttons to register or login at the top.  There is a search function that will do a case insensitive search (i_contains) against both users and journals (title, body, and tags).  The section on the right shows the latest few available public journals from any user on the site.

## Feed

This page shows all public journals from your followed users in reverse chronological order.  Inaccessible to unauthenticated users.  

## Profile

On a user's profile you can see all of their public journals, their profile picture, and you can follow or unfollow them.  When a user is looking at their own profile they can see all of their own public or private journals, filter them by public or private, and edit their profile picture.

## Journal

The detailed page for a journal where you can see the title, body, and tags for a journal in full.  If a user is looking at their own journal they can delete it if they so choose.

## Other

Other smaller pages include a login, and register page, and a few pages for changing or resetting a password.  Changing and resetting passwords does work, but unfortunately I haven't set up a service to actually send the emails to do so to the users, so they're inaccessible.

##### There are several remaining issues with the site, but the most noticeable upon loading the site up is that user's profile pictures disappear when heroku shuts down the server.  This is known, and noted in issue #5
