# Instructions on setup to make this code run available at:
# https://github.com/LucaDantas/WHMCS_WebScraper/blob/main/README.md#how-to-run-the-program
# Remember that this uses firefox and geckodriver, so it won't work in chrome

# summary of the instructions:
# For this code to run you need to have firefox installed and install its respective selenium driver (geckodriver)
# you also need to add a config.py file with the username and password to access WHMCS
# Just create a variable called username and a variable called password in the config.py file and add it to the same folder
# you also need to install selenium and requests libraries from pip

import config_whm as config
# import requests
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

csv_administrators = "../raw/websites.csv"

# gets the information I want from the website configurations page, if login/email doesn't exist it just leaves it blank but prints the rest of the information
def goto_configurations(driver, csvfile):
    title = driver.find_element(By.ID, 'field_title').get_attribute("value")
    domain = driver.find_element(By.CSS_SELECTOR, 'div.i_links table.i_simpletable a.i_link').text

    if (len(driver.find_elements(By.ID, 'field_login')) > 0):
        login = driver.find_element(By.ID, 'field_login')
    if (len(driver.find_elements(By.ID, 'field_email')) > 0):
        email = driver.find_element(By.ID, 'field_email')

    v_login = ""
    v_email = ""
    if (len(driver.find_elements(By.ID, 'field_login')) > 0):
        v_login = login.get_attribute("value")
    if (len(driver.find_elements(By.ID, 'field_email')) > 0):
        v_email = email.get_attribute("value")

    csvfile.writerow((domain, title, v_login, v_email))

def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    with launch_browser() as driver, open(csv_administrators, 'w') as admf:
        csvfile = csv.writer(admf)

        # goes directly to the correct page
        driver.get('https://carleton.reclaimhosting.com:2087/cpsess8481751054/installatron/index.cgi#/installs?filter-ownedaccounts=')
        driver.maximize_window()

        # logs in
        driver.find_element(By.NAME, 'user').send_keys(config.username)
        driver.find_element(By.NAME,'pass').send_keys(config.password)
        driver.find_element(By.NAME,'login').click()
 
        time.sleep(20)

        csvfile.writerow(("Domain", "Title", "Administrator Username", "Adm Email"))

        # It iterates through the list of pages on the bottom (1-100, 101-200, ...) to be able to navigate through the pages and get every website
        for i in range(0, len(driver.find_elements(By.CSS_SELECTOR, "select[onchange='i_redirectLocation(buildQuery({p:this.options[this.selectedIndex].value}));'] option"))):

            if i > 0: # change to the correct page
                # give it a lot of time to sleep and select the correct page because this was giving me a lot of trouble without the time.sleep, and it will only happen a few times so it's not that slow
                time.sleep(10)
                driver.find_elements(By.CSS_SELECTOR, "select[onchange='i_redirectLocation(buildQuery({p:this.options[this.selectedIndex].value}));'] option")[i].click()
                time.sleep(10)

            # this is how to find the pages, make a list of the li's
            services = driver.find_elements(By.CSS_SELECTOR, '#i_content .i_myapps_detail li')
            for service in services:
                # every page has a subheader in WHM which is also a li but not really a clickable page, so we ignore it
                if service.get_attribute("class") == "i_myapps_table_subheader":
                    print(service.text) # print this just to know which website we're visiting right now as a log
                    continue

                # gets the link to the configurations page
                link = service.find_element(By.CSS_SELECTOR, ".i_header_right a[data-descr='view/edit details']").get_attribute("href")

                # open it in a new window and switch the driver there
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)

                while(len(driver.find_elements(By.ID, 'field_title')) == 0):
                    time.sleep(0.5)

                # get the information I need from the configuration page
                goto_configurations(driver, csvfile)
 
                # close the configuration window and come back to the main page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    main()
