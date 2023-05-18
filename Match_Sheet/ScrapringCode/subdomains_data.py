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

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

# csv file that the output will be redirected to
csv_subd = "../raw/subdomains.csv"

def goto_subd(driver, csvfile, domain_name):
    # wait for the page to load
    while(len(driver.find_elements(By.ID, 'item_subdomains')) == 0):
        time.sleep(0.5)

    # click into the subdomains page
    driver.find_element(By.ID, 'item_subdomains').click()

    subdomains_table = driver.find_element(By.CSS_SELECTOR, '#subdomaintbl tbody')

    if subdomains_table.text == "No Subdomains are configured.":
        # csvfile.writerow((domain_name, "No subdomains")) # I wrote a message to say that there are no subdomains but you can also just ignore it
        pass
    else:
        # get all the subdomains and write them to the csv file
        for row in subdomains_table.find_elements(By.CSS_SELECTOR, 'tr'):
            subdomain = row.find_element(By.CSS_SELECTOR, 'td').text # finds the first, which is the name of the subdomain
            csvfile.writerow((domain_name, subdomain))

def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    with launch_browser() as driver, open(csv_subd, 'w') as subdf:
        csvfile = csv.writer(subdf)

        # goes directly to the correct page - Accounts list in CPanel
        driver.get('https://carleton.reclaimhosting.com:2087/cpsess4529333244/scripts4/listaccts?login=1&post_login=9355209981466')
        driver.maximize_window()

        # logs in
        driver.find_element(By.NAME, 'user').send_keys(config.username)
        driver.find_element(By.NAME,'pass').send_keys(config.password)
        driver.find_element(By.NAME,'login').click()
 
        time.sleep(5)

        # click the button to show all the cpanels in the same page
        page_num = driver.find_element(By.CSS_SELECTOR, '#page-size-selector input[type="text"]')
        page_num.clear()
        page_num.send_keys(1000) # I want to make all the domains visible at once
        page_num.send_keys('\ue007')

        time.sleep(5)

        csvfile.writerow(("Domain", "Subdomain"))

        table = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[5]/div[3]/table/tbody')

        for row in table.find_elements(By.CSS_SELECTOR,'tr'):
            domain_name = row.find_elements(By.CSS_SELECTOR, 'td')[1].find_element(By.CSS_SELECTOR, 'a').text

            # the cpanel button is not a html link, but a thing that the user interacts via a mouse click and is processed by
            # javascript, so the element actually needs to be visible on the screen, so I set it to scroll everytime so that
            # the element can be seen and can be clicked
            driver.execute_script("window.scrollBy(0,35)");
            
            # open the cpanel window
            row.find_elements(By.CSS_SELECTOR, 'td')[2].click()

            # switch to the other window
            driver.switch_to.window(driver.window_handles[1])

            goto_subd(driver, csvfile, domain_name)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    main()
