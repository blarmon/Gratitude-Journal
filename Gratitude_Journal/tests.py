from django.test import LiveServerTestCase
from journals.models import Journal
from journals.forms import JournalForm
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class UserTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe')
        self.browser.implicitly_wait(2)


    def tearDown(self):
        self.browser.quit()

    def test_new_user_creates_journal(self):
        # Becky is a busy professional who wants to find more gratitude in her day to day life
        # and worry less about the future.  She visits the home page of our working title Gratitude Journal Site.

        home_page = self.browser.get(self.live_server_url + '')

        # As on every page, Becky sees the brand in the navbar from 'base.html' at the top of the page.

        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')

        # Because she doesn't have an account, she is redirected to an "explore page", which allows her to search other peoples' journals by title or tag,
        # and displays a few select recent journals.  Because she is not logged in, she sees a quick explanation of the site at the top,  as well as buttons
        #  to log in or sign up.  She chooses to sign up for a new account, so she clicks the "Register" button.

        self.assertEqual(self.browser.current_url, self.live_server_url + '/explore/')
        self.assertEqual(self.browser.title, 'Explore')

        log_in_button = self.browser.find_element_by_link_text('Log In')
        register_button = self.browser.find_element_by_link_text('Register')
        register_button.click()

        # After entering her username, password, and email, she is redirected to her home page.

        register_form = self.browser.find_element_by_id('user-registration-form')
        register_form.find_element_by_id('id_username').send_keys('functional_test_user')
        register_form.find_element_by_id('id_password1').send_keys('user_password')
        register_form.find_element_by_id('id_password2').send_keys('user_password')

        register_form.find_element_by_class_name('submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

        self.journal1 = Journal.objects.create(user=User.objects.get(username='functional_test_user'), title='journal 1 title', body='journal 1 body', public=False, date=now()-timedelta(days=1))
        self.journal2 = Journal.objects.create(user=User.objects.get(username='functional_test_user'), title='journal 2 title', body='journal 2 body', public=True, date=now()-timedelta(days=365))
        self.journal3 = Journal.objects.create(user=User.objects.get(username='functional_test_user'), title='journal 3 title', body='journal 3 body', public=False, date=now()-timedelta(days=12))

        # From here (the index page) she can create a new (rich text) blog post, and see her 3 most recent posts beneath that (including her latest post, on page refresh).

        self.browser.find_element_by_id('id_title').send_keys('My Post Title')
        self.browser.find_element_by_id('id_public').click()
        self.browser.find_element_by_id('id_body').send_keys('My Post Body')
        self.browser.find_element_by_id('submit').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

        recent_posts = self.browser.find_elements_by_css_selector('.recent_post')

        self.assertEqual(len(recent_posts), 3)

        self.assertEqual(len(self.browser.find_elements_by_xpath("//*[contains(text(), 'journal 1 title')]")), 1)
        self.assertEqual(len(self.browser.find_elements_by_xpath("//*[contains(text(), 'My Post Body')]")), 1)

        # She also can see her latest post on the explore page now, as well as her other public journals.

        self.browser.find_element_by_link_text('Explore').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/explore/')

        public_posts = self.browser.find_elements_by_css_selector('.public_post')
        self.assertEqual(len(public_posts), 2)

class UserProfileTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe')
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_user_explores_their_own_profile(self):
        #the user will see an archive of ALL of their posts (public and private), ordered by date.  clicking on one will take them to the page to view a single journal.  they can filter for public or private only, if they so wish.
        home_page = self.browser.get(self.live_server_url + '')
        #users should start on the explore page when they are not logged in
        self.assertEqual(self.browser.current_url, self.live_server_url + '/explore/')

        #she clicks the register button to create a new user.
        register_button = self.browser.find_element_by_link_text('Register')
        register_button.click()

        #she fills out the form and submits it.  she is redirected to her user page.
        register_form = self.browser.find_element_by_id('user-registration-form')
        register_form.find_element_by_id('id_username').send_keys('functional_test2_user')
        register_form.find_element_by_id('id_password1').send_keys('user_password')
        register_form.find_element_by_id('id_password2').send_keys('user_password')
        register_form.find_element_by_class_name('submit').click()

        self.journal1 = Journal.objects.create(user=User.objects.get(username='functional_test2_user'),
                                               title='journal 1 title', body='journal 1 body', public=False,
                                               date=now() - timedelta(days=-1))
        self.journal2 = Journal.objects.create(user=User.objects.get(username='functional_test2_user'),
                                               title='journal 2 title', body='journal 2 body', public=True,
                                               date=now() - timedelta(days=-365))
        self.journal3 = Journal.objects.create(user=User.objects.get(username='functional_test2_user'),
                                               title='journal 3 title', body='journal 3 body', public=False,
                                               date=now() - timedelta(days=-12))
        self.journal4 = Journal.objects.create(user=User.objects.get(username='functional_test2_user'),
                                               title='journal 4 title', body='journal 4 body', public=True,
                                               date=now() - timedelta(days=-200))
        self.journal5 = Journal.objects.create(user=User.objects.get(username='functional_test2_user'),
                                               title='journal 5 title', body='journal 5 body', public=True,
                                               date=now() - timedelta(days=-200))

        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

        #she finds the profile button in the navbars dropdown and clicks it.  on this page she sees all of the titles of her journals (TODO? maybe add the first 100 words of the body?), ordered by date.
        self.browser.find_element_by_xpath("//*[contains(text(), 'Dropdown button')]").click()
        self.browser.find_element_by_xpath("//*[contains(text(), 'Profile')]").click()

        user_id = str(User.objects.get(username='functional_test2_user').id)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/profile/' + user_id)

        user_journals = self.browser.find_elements_by_class_name('journal_title')

        self.assertEqual(len(user_journals), 5)

        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 2 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 1 title')]")

        # she clicks on the filter to only see her private journals
        self.browser.find_element_by_id('private_radio').click()
        user_journals = self.browser.find_elements_by_class_name('journal_title')
        self.assertEqual(len(user_journals), 2)
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 1 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 3 title')]")

        # she clicks on the filter to only see her public journals
        self.browser.find_element_by_id('public_radio').click()
        user_journals = self.browser.find_elements_by_class_name('journal_title')

        self.assertEqual(len(user_journals), 3)
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 2 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 4 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 5 title')]")

        # she clicks on the filter to see all of her journals
        self.browser.find_element_by_id('all_radio').click()
        user_journals = self.browser.find_elements_by_class_name('journal_title')
        self.assertEqual(len(user_journals), 5)
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 2 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 4 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 5 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 1 title')]")
        self.browser.find_element_by_xpath("//*[contains(text(), 'journal 3 title')]")

        # she can click a journal title, and be taken to a page that displays that journal.
        journal_title = self.browser.find_elements_by_class_name('journal_title')[3]
        journal_title_text = str(journal_title.text)
        journal_title.click()

        clicked_journal_id = str(Journal.objects.get(title=journal_title_text).id)

        clicked_journal = Journal.objects.get(title=journal_title_text)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/journal/' + clicked_journal_id)

        self.browser.find_element_by_xpath("//*[contains(text(), '" + clicked_journal.title + "' )]")
        self.browser.find_element_by_xpath("//*[contains(text(), '" + clicked_journal.body + "' )]")
        self.browser.find_element_by_id("journal_date")

class UserProfileTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe')
        self.browser.implicitly_wait(2)
        User.objects.get_or_create(username='testuser_profile_visited')[0]
        Journal.objects.create(user=User.objects.get(username='testuser_profile_visited'), title='journal 1 title',
                               body='journal 1 body', public=True, date=now() - timedelta(days=1))
        Journal.objects.create(user=User.objects.get(username='testuser_profile_visited'), title='journal 2 title',
                               body='journal 2 body', public=True, date=now() - timedelta(days=1))
        Journal.objects.create(user=User.objects.get(username='testuser_profile_visited'), title='journal 3 title',
                               body='journal 3 body', public=False, date=now() - timedelta(days=1))

    def tearDown(self):
        self.browser.quit()

    def test_user_explores_another_users_profile(self):

        home_page = self.browser.get(self.live_server_url + '')

        # the user registers an account

        register_button = self.browser.find_element_by_link_text('Register')
        register_button.click()

        register_form = self.browser.find_element_by_id('user-registration-form')
        register_form.find_element_by_id('id_username').send_keys('functional_test_user')
        register_form.find_element_by_id('id_password1').send_keys('user_password')
        register_form.find_element_by_id('id_password2').send_keys('user_password')

        register_form.find_element_by_class_name('submit').click()

        # They are taken to their home page

        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

        # They click the explore page and see public posts from all users.

        self.browser.find_element_by_link_text('Explore').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/explore/')

        public_journals = self.browser.find_elements_by_class_name('journal_container')
        self.assertEqual(len(public_journals), 2)

        # They click on a users username and are taken to their profile, where they see all of that users public post titles, as well as that users username at the top (TODO? and maybe a small 100 word blurb)

        public_journal_user = self.browser.find_elements_by_class_name('journal_user')
        public_journal_user[0].click()

        user_clicked_id = str(User.objects.get(username='testuser_profile_visited').id)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/profile/' + user_clicked_id)

        self.browser.find_element_by_xpath("//*[contains(text(), 'testuser_profile_visited')]")

        journal_one = self.browser.find_element_by_link_text('journal 1 title')
        journal_one_text = journal_one.text
        self.browser.find_element_by_link_text('journal 2 title')
        self.browser.find_element_by_link_text('journal 3 title')
        self.browser.find_element_by_link_text('journal 4 title')

        # They click on a journal from that user and are taken to the detailed journal page for the clicked journal

        journal_one.click()

        clicked_journal_id = str(Journal.objects.get(title=journal_one_text).id)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/journal/' + clicked_journal_id)

        clicked_journal = Journal.objects.get(title=journal_one_text)

        detailed_journal_title = self.browser.find_element_by_id('journal_title').text
        detailed_journal_body = self.browser.find_element_by_id('journal_body').text

        self.assertEqual(clicked_journal.title, detailed_journal_title)
        self.assertEqual(clicked_journal.body, detailed_journal_body)



    # def test_user_explores_aboutslashresearch_page(self):
    #     #user goes to the research (working title) page.
    #     pass

# class UnauthenticatedUserTestCase(StaticLiveServerTestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe')
#         self.browser.implicitly_wait(2)
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def test_unauthenticated_user_uses_explore_page(self):
#         pass