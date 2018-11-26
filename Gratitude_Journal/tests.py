from django.test import LiveServerTestCase

from selenium import webdriver

class UserTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe')
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_new_user_creates_journal(self):
        # Becky is a professional who wants to find more gratitude in her day to day life
        # and worry less about the future.  She visits the home page of our working title Gratitude Journal Site.

        home_page = self.browser.get(self.live_server_url + '/')

        # Because she doesn't have an account, she is redirected to an "explore page", which allows her to search other peoples' journals by title or tag,
        # and displays a few select recent journals.  Because she is not logged in, she sees a quick explanation of the site at the top,  as well as buttons
        #  to log in or sign up.  She chooses to sign up for a new account, so she clicks the "Sign up" button.

        self.fail('incomplete test')

        # After entering her username, password, and email, she is redirected to her home page.  From here she can create a new (rich text) blog post,
        #  and see her 3 most recent posts beneath that.

        # She decides to create a new post.  She enters a title (optional), it's dated with today's date automatically, and she enters the body of the post.
        # Using a radio button she decides to make her post public, so that others can share in her gratitude and find inspiration.  She clicks the submit button.

        # She is successfully brought back to her user home page.