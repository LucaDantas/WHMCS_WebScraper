# Instructions on setup to make this code run available at:
# https://github.com/LucaDantas/WHMCS_WebScraper/blob/main/README.md#how-to-run-the-program
# Remember that this uses firefox and geckodriver, so it won't work in chrome

# summary of the instructions:
# For this code to run you need to have firefox installed and install its respective selenium driver (geckodriver)
# you also need to add a config.py file with the username and password to access WHMCS
# Just create a variable called username and a variable called password in the config.py file and add it to the same folder
# you also need to install selenium and requests libraries from pip

import config_whm as config
import requests
import csv
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# csv file that the output will be redirected to
csv_domains = "../raw/domains.csv"

def launch_browser(profile):
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s, options=profile)
    return driver

def main():
    # changes the firefox options to be able to download the file to the current working folder
    profile = Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

    # launches browser
    with launch_browser(profile) as driver:

        # goes directly to the correct page - Accounts list in CPanel
        driver.get('https://carleton.reclaimhosting.com:2087/cpsess4529333244/scripts4/listaccts?login=1&post_login=9355209981466')
        driver.maximize_window()

        # logs in
        driver.find_element(By.NAME, 'user').send_keys(config.username)
        driver.find_element(By.NAME,'pass').send_keys(config.password)
        driver.find_element(By.NAME,'login').click()
 
        time.sleep(3)

        driver.find_element(By.CSS_SELECTOR, '.controls > a:nth-child(1)').click() # click the button to download it

        time.sleep(5)

    # change the name of the file from root (which is what we are given from WHM to the name we want)
    os.rename('root.csv', csv_domains)


if __name__ == '__main__':
    main()
