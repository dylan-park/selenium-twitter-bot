from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options
import time

options = Options()
# TODO: Make this less user centric, universal chrome binary
options.binary_location = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\new_chrome.exe"
options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=options, executable_path=r'./chromedriver/chromedriver.exe')
driver.get('http://google.com/')
print("Chrome Browser Invoked")


class TwitterBot:
    """
    A Bot class that provide features of:
        - Logging into your Twitter account
        - Liking tweets of your homepage
        - Searching for some keyword or hashtag
        - Liking tweets of the search results
        - Posting tweets
        - Logging out of your account

    ........

    Attributes
    ----------
    user : str
        user user for Twitter account
    password : str
        user password for Twitter account
    bot : WebDriver
        webdriver that carry out the automation tasks
    is_logged_in : bool
        boolean to check if the user is logged in or not

    Methods ------- login() logs user in based on user and password provided during initialisation logout() logs
    user out search(query: str) searches for the provided query string like_tweets(cycles: int) loops over number of
    cycles provided, scrolls the page down and likes the available tweets on the page in each loop pass
    """

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.bot = driver
        self.is_logged_in = False

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(4)

        try:
            user = bot.find_element("xpath", "//input[@name='text']")
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            user = bot.find_element("xpath", "//input[@name='text']")

        user.clear()
        user.send_keys(self.user)
        user.send_keys(keys.Keys.RETURN)
        time.sleep(3)

        try:
            password = bot.find_element("xpath", "//input[@name='password']")
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            password = bot.find_element("xpath", "///input[@name='password']")

        password.clear()
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        time.sleep(5)
        self.is_logged_in = True

    def logout(self):
        if not self.is_logged_in:
            return

        bot = self.bot
        bot.get('https://twitter.com/home')
        time.sleep(4)

        try:
            bot.find_element("xpath", "//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element("xpath", "//div[@data-testid='SideNav_AccountSwitcher_Button']").click()

        time.sleep(1)

        try:
            bot.find_element("xpath", "//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            bot.find_element("xpath", "//a[@data-testid='AccountSwitcher_Logout_Button']").click()

        time.sleep(3)

        try:
            bot.find_element("xpath", "//div[@data-testid='confirmationSheetConfirm']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element("xpath", "//div[@data-testid='confirmationSheetConfirm']").click()

        time.sleep(3)
        self.is_logged_in = False

    def search(self, query=''):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            searchbox = bot.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']")
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            searchbox = bot.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']")

        searchbox.clear()
        searchbox.send_keys(query)
        searchbox.send_keys(keys.Keys.RETURN)
        time.sleep(10)

    def like_tweets(self, cycles=10):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        for i in range(cycles):
            try:
                bot.find_element("xpath", "//div[@data-testid='like']").click()
            except common.exceptions.NoSuchElementException:
                time.sleep(3)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight/1.5)')
                time.sleep(3)
                bot.find_element("xpath", "//div[@data-testid='like']").click()

            time.sleep(1)
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight/1.5)')
            time.sleep(5)

    def post_tweet(self, tweet_body):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            bot.find_element("xpath", "//a[@data-testid='SideNav_NewTweet_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element("xpath", "//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4)
        body = tweet_body

        try:
            bot.find_element("xpath", "//div[@role='textbox']").click()
            bot.find_element("xpath", "//div[@role='textbox']").send_keys(body)
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element("xpath", "//div[@role='textbox']").click()
            bot.find_element("xpath", "//div[@role='textbox']").send_keys(body)

        time.sleep(4)
        # bot.find_element_by_class_name("notranslate").send_keys(keys.Keys.ENTER)
        bot.find_element("xpath", "//div[@data-testid='tweetButton']").click()
        time.sleep(4)
