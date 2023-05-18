# Instructions on setup to make this code run available at:
# https://github.com/LucaDantas/WHMCS_WebScraper/blob/main/README.md#how-to-run-the-program
# Remember that this uses firefox and geckodriver, so it won't work in chrome

# summary of the instructions:
# For this code to run you need to have firefox installed and install its respective selenium driver (geckodriver)
# you also need to add a config.py file with the username and password to access WHMCS
# Just create a variable called username and a variable called password in the config.py file and add it to the same folder
# you also need to install selenium and requests libraries from pip

import config_whmcs as config
import requests
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

# csv file that the data will be added to
csv_clients = "../raw/clients.csv"

def get_informations(driver, out):
    # wait until the page is loaded so that I can begin getting the data I want
    while(len(driver.find_elements(By.CSS_SELECTOR, 'textarea')) == 0):
        time.sleep(0.5)

    # gets all the information, I avoided using XPATHs because they are too dependent on the structure of the page and it broke a few times
    user_id = int(driver.find_element(By.CSS_SELECTOR, '#userId').text)

    table_stats = driver.find_element(By.CLASS_NAME, 'clientssummarystats')
    first_name = table_stats.find_elements(By.CSS_SELECTOR, 'tr')[0].find_elements(By.CSS_SELECTOR, 'td')[1].text
    last_name  = table_stats.find_elements(By.CSS_SELECTOR, 'tr')[1].find_elements(By.CSS_SELECTOR, 'td')[1].text
    email      = table_stats.find_elements(By.CSS_SELECTOR, 'tr')[3].find_elements(By.CSS_SELECTOR, 'td')[1].text

    signup_date = driver.find_element(By.CSS_SELECTOR, 'div.row:nth-child(2) > div:nth-child(2) > div:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text

    role = driver.find_element(By.CSS_SELECTOR, 'textarea').text

    status = driver.find_element(By.CSS_SELECTOR, 'div.row:nth-child(2) > div:nth-child(2) > div:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text

    out.writerow((user_id, first_name, last_name, email, signup_date, role, status))

def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    with launch_browser() as driver, open(csv_clients, 'w') as clif:
        clients = csv.writer(clif)

        driver.get('https://sites.carleton.edu/manage/whmcs-admin/login.php?logout=1')
        driver.maximize_window()

        # logs in
        driver.find_element(By.NAME, 'username').send_keys(config.username)
        driver.find_element(By.NAME,'password').send_keys(config.password)
        driver.find_element(By.CSS_SELECTOR,'input[value=Login]').click()
        
        # nagivate to clients page
        driver.find_element(By.ID, 'Menu-Clients').click()

        # enables the view of inactive accounts
        driver.find_element(By.CLASS_NAME, 'bootstrap-switch').click()

        time.sleep(1)

        for i in range(100): # I've set 100 as a safety number in case the loop doesn't stop for some reason

            # give it some time to load
            time.sleep(3)

            # selects every user and opens and then scraps their respective pages
            for user in driver.find_element(By.ID, "sortabletbl0").find_elements(By.CSS_SELECTOR, "tr")[1:]:
                # opens the page of the user in a new window
                user.find_element(By.CSS_SELECTOR, "a").send_keys('\ue009' + '\ue007') # Control + Enter
     
                # goes to the user window, scrapes it and comes back
                driver.switch_to.window(driver.window_handles[1])

                get_informations(driver, clients)
     
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            # while there is a link to go to the next page I click, otherwise I break to stop
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page").click()
            except:
                break

if __name__ == '__main__':
    main()
