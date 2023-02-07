from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os

url = 'https://twitter.com/login'

# change this path to where the chromedriver is on your machine
CHROMEDRIVERPATH = '/Users/rmiriuk/chromedriver'

# change this to your username and password
userUsername = os.environ['EMAIL']
userPassword = os.environ['PASSWORD']


def tweety(text):
    browser = webdriver.Chrome()
    browser.get(url)

    browser.implicitly_wait(5)

    user = browser.find_element_by_name('session[username_or_email]')
    user.send_keys(userUsername)

    password = browser.find_element_by_name('session[password]')
    password.send_keys(userPassword)
    password.send_keys(Keys.ENTER)

    browser.implicitly_wait(5)
    browser.get('https://twitter.com/intent/tweet')
    browser.implicitly_wait(1)
    tweet = browser.find_element_by_css_selector("textarea[data-testid='tweetTextarea_0']")
    tweet.send_keys(str(text))

    button = browser.find_element_by_css_selector("div[data-testid='tweetButton']")
    button.click()

    browser.close()
