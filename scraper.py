# Written by Luca Araújo, '26
# September 29, 2022

import config
import requests
import csv
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

# unconmment the next line if using chrome
# from selenium.webdriver.firefox.service import Service

def scrape(source, csv_file):
    soup = BeautifulSoup(source, 'html.parser')
    summary_stats = soup.find(class_="clientssummarystats")

    rows = summary_stats.find_all('tr')
    first_name = rows[0].find_all('td')[1].get_text()
    last_name = rows[1].find_all('td')[1].get_text()
    email_address = rows[3].find_all('td')[1].get_text()

    products = []
    
    # looks at all the products/services of a user
    accounts_filterable = soup.find(class_="filterable")
    for column in accounts_filterable.find_all('tr')[1:]:
        try:
            products.append(column.find_all('td')[2].find('a').get_text())
        except:
            break
    
    admin_notes = soup.find('textarea', class_="form-control").get_text()
    if admin_notes == '':
        admin_notes = '#'

    line = first_name + ',' + last_name + ',' + email_address + ',' + admin_notes
    for i in range(len(products)):
        line += ',' + products[i]
    line += '\n'

    csv_file.write(line)

# lauches the webdriver.
# if you want to use firefox uncomment the first two lines and comment the respective lines for chrome
def launch_browser():
    # s=Service('./geckodriver')
    # driver = webdriver.Firefox(service=s)

    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)

    return driver

def main():
    # launches browser
    driver = launch_browser()
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

    with open('data.csv', 'w') as csv_file:
        # parse each page with the clients individually
        for i in range(100): # I've set 100 as a safety number in case the loop doesn't stop for some reason

            # selects every user and opens and then scraps their respective pages
            for user in driver.find_element(By.ID, "sortabletbl0").find_elements(By.CSS_SELECTOR, "tr")[1:]:
                # opens the page of the user in a new window
                user.find_element(By.CSS_SELECTOR, "a").send_keys('\ue009' + '\ue007') # Control + Enter
                
                # goes to the user window, scrapes it and comes back
                driver.switch_to.window(driver.window_handles[1])

                # We need to give it a few seconds to load the page
                time.sleep(2)
                
                # scrape with beautiful soup
                scrape(driver.page_source, csv_file)
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            # while there is a link to go to the next page I click, otherwise I break to stop
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page").click()
            except:
                break
        

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
