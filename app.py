from flask import Flask, request, redirect, session
from flask_session import Session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Your Keepa credentials
KEEPA_USERNAME = 'xstore4u1@gmail.com'
KEEPA_PASSWORD = '03332803108+'

# Path to your ChromeDriver
CHROMEDRIVER_PATH = r'C:\chromedriver\chromedriver\chromedriver.exe'  # Ensure the full path is correct

def init_browser():
    options = Options()
    options.headless = True
    service = Service(CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=service, options=options)
    return browser

def login_to_keepa(browser):
    browser.get('https://keepa.com/#!')
    
    # Wait for the login overlay to appear and be visible
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'loginOverlay')))
    
    # Wait for the login form elements to be visible
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'username')))
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'submitLogin')))
    
    # Find the elements
    username_input = browser.find_element(By.ID, 'username')
    password_input = browser.find_element(By.ID, 'password')
    submit_button = browser.find_element(By.ID, 'submitLogin')

    # Enter credentials and submit the form
    username_input.send_keys(KEEPA_USERNAME)
    password_input.send_keys(KEEPA_PASSWORD)
    submit_button.click()
    
    # Wait until logged in, which can be identified by a specific element or URL change
    WebDriverWait(browser, 10).until(EC.url_contains('dashboard'))

@app.route('/')
def home():
    if 'browser' not in session:
        browser = init_browser()
        login_to_keepa(browser)
        session['browser'] = browser

    browser = session['browser']
    browser.get('https://keepa.com/')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    page_source = browser.page_source

    return page_source

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if 'browser' not in session:
        browser = init_browser()
        login_to_keepa(browser)
        session['browser'] = browser

    browser = session['browser']
    url = f'https://keepa.com/{path}'
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    page_source = browser.page_source

    return page_source

if __name__ == '__main__':
    app.run(debug=True)
