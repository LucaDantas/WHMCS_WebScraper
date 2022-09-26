import config
import requests
import csv
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

def scrape(soup):
    pass

# lauches the webdriver. if using different diver change in line 's=Service('./chromedriver')'.
def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    driver = launch_browser()
    driver.get('https://sites.carleton.edu/manage/whmcs-admin/login.php?logout=1')

    # logs in
    driver.find_element(By.NAME, 'username').send_keys(config.username)
    driver.find_element(By.NAME,'password').send_keys(config.password)
    driver.find_element(By.CSS_SELECTOR,'input[value=Login]').click()
    
    # nagivate to clients page
    driver.find_element(By.ID, 'Menu-Clients').click()

    driver.find_element(By.CLASS_NAME, 'bootstrap-switch').click()

    # parse each page with the clients individually
    for i in range(100): # I've set 100 as a safety number in case the loop doesn't stop for some reason

        # selects every user and opens and then scraps their respective pages
        for user in driver.find_element(By.ID, "sortabletbl0").find_elements(By.CSS_SELECTOR, "tr")[1:]:
            # opens the page of the user in a new window
            user.find_element(By.CSS_SELECTOR, "a").send_keys('\ue009' + '\ue007') # Control + Enter
            
            # goes to the user window, scrapes it and comes back
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            scrape(BeautifulSoup(driver.page_source, 'html.parser'))
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
        
        # while there is a link to go to the next page I click, otherwise I break to stop
        try:
            driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page").click()
        except:
            break
        

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
