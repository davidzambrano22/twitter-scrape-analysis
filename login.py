
from email.policy import default
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import argparse
import sys

#___________________________________________________________________________________________
"""This class  creates the element that represents the driver"""
def Driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver
#___________________________________________________________________________________________
"""En esta función se utilizan el usuario y contraseña y el driver de la clase driver"""

def Login(email, password, file):
    url = 'https://twitter.com/i/flow/login'
    try:
        #Se utiliza la clase Driver
        driver = Driver()
        driver.get(url)
        time.sleep(10)
        #go_to_login(driver)
        #time.sleep(10)
        input_email(driver, email)
        time.sleep(10)
        #if not driver.find_element_by_xpath("//input[@autocomplete='current-password']"):
            #Check if driver opens twitter unusual activity page
            #if driver.find_element_by_xpath("//input[@autocomplete='on']"):
             #   confirmation_element = driver.find_element_by_xpath("//input[@autocomplete='on']")
              #  confirmation_element.send_keys(phone_number)
               # confirmation_element.send_keys(Keys.ENTER) 
        input_password(driver, password)
        time.sleep(10)
        print(driver.current_url)
        search(driver)
        print(driver.current_url)
        find_tweets(driver, file)
    except Exception as e:
        print(e)

#___________________________________________________________________________________________
"""Function to input email to login"""

def input_email(driver, email):
    #Introducir control para email inválidos con regex
    email_element = driver.find_element_by_xpath("//input[@autocomplete='username']")
    email_element.send_keys(email)
    email_element.send_keys(Keys.ENTER)


#___________________________________________________________________________________________
"""Function to input the password"""

def input_password(driver, password):
    password_element = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
    password_element.send_keys(password)
    password_element.send_keys(Keys.ENTER)

#___________________________________________________________________________________________
"""Do a search in twitter"""

def search(driver):
    input_element = driver.find_element_by_xpath("//input[@placeholder='Buscar en Twitter']")
    input_element.send_keys('protestas bogota')
    input_element.send_keys(Keys.ENTER)
    
#___________________________________________________________________________________________
"""Find the tweets"""

def find_tweets(driver, file):
    #First alternative
    #tweet_elements = driver.find_elements_by_xpath("//div[@class='css-1dbjc4n r-j5o65s r-qklmqi r-1adg3ll r-1ny4l3l']")
    ####alternativa donde se una clase proxima a los contenedores
    for scroll in range(10):
        try:
            tweets = driver.find_elements_by_xpath("//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
            time.sleep(10)
            if not tweets:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(30)
                tweets = driver.find_elements_by_xpath("//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
            print('n. tweets = ', len(tweets))
            if not tweets:
                continue
            get_text(tweets, file)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(30)
        except Exception as e:
            print(Exception, 'Error: No tweets in this scroll')


#__________________________________________________________________________________________
"""Get tweets text"""

def get_text(tweets, file):
    scraped_tweets = set()
    for tweet in tweets:
        tweet_text = ''
        spans = tweet.find_elements_by_tag_name('span')
        for span in spans:
            phrase = span.text
            tweet_text += phrase
            scraped_tweets.add(tweet_text)
    #print the joined tweet text into a document
    print(len(scraped_tweets))
    for tweet in scraped_tweets:
        print(tweet, file= file)
        print('--------------------------------------------------------------------------------------', file = file)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type= str, help = 'User name')
    parser.add_argument('-p', type= str, help = 'User password')
    parser.add_argument('-o', type= argparse.FileType('w'), default = sys.stdout, help = 'Outpot file name')
    args = parser.parse_args()
    Login(args.n, args.p, args.o)