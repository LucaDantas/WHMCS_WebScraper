# Written by Luca Araújo, '26
# Fall, 2022

# This code scrapes the information of product/services on whmcs and outputs it to csv_output file
# does not use beautiful soup, only selenium

import config
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

csv_output = 'data.csv'

def scrape_service(driver, csv_file, given_name, surname, email):
    domain = driver.find_element(By.CSS_SELECTOR, "[name='domain']").get_attribute('value')
    regdate = driver.find_element(By.CSS_SELECTOR, "[name='regdate']").get_attribute('value')
    
    writer = csv.writer(csv_file)
    writer.writerow((given_name, surname, email, domain, regdate))

def get_services(driver, csv_file, given_name, surname, email):
    driver.find_element(By.ID, 'clientTab-4').click()
    while(len(driver.find_elements(By.XPATH, '/html/body/div[8]/div[1]/div')) == 0):
        time.sleep(0.5)
    if(len(driver.find_elements(By.ID, 'servicecontent')) == 0):
        print("This user has no services")
    else:
        element = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/div[1]/div[1]/div/div[1]/form/div/div[1]')

        actions = ActionChains(driver)
        actions.click(element).perform()
        
        services_list = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/div[1]/div[1]/div/div[1]/form/div').find_element(By.CLASS_NAME, 'selectize-dropdown-content').find_elements(By.CSS_SELECTOR, 'div')
        
        sz = len(services_list)

        actions.click(element).perform()

        for i in range(sz):
            element = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/div[1]/div[1]/div/div[1]/form/div/div[1]')
            actions.click(element).perform()

            service = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/div[1]/div[1]/div/div[1]/form/div').find_element(By.CLASS_NAME, 'selectize-dropdown-content').find_elements(By.CSS_SELECTOR, 'div')[i]

            domain = service.text.split(' - ')[1]

            # goes to the page of the domain we want now
            actions.send_keys(domain).key_down('\ue007').perform()

            # waits for the page to load
            opa = driver.find_elements(By.CSS_SELECTOR, "[name='domain']")
            while(len(opa) == 0 or opa[0].get_attribute('value') != domain):
                time.sleep(0.5)
                opa = driver.find_elements(By.CSS_SELECTOR, "[name='domain']")

            # scrape the data from that service
            print("SCRAPING THIS SERVICE")
            scrape_service(driver, csv_file, given_name, surname, email)

# lauches the webdriver.
def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    with launch_browser() as driver:
        driver.get('https://sites.carleton.edu/manage/whmcs-admin/login.php')
        driver.maximize_window()

        # logs in
        driver.find_element(By.NAME, 'username').send_keys(config.username)
        driver.find_element(By.NAME,'password').send_keys(config.password)
        driver.find_element(By.CSS_SELECTOR,'input[value=Login]').click()
        
        # nagivate to clients page
        driver.find_element(By.ID, 'Menu-Clients').click()

        # enables the view of inactive accounts
        driver.find_element(By.CLASS_NAME, 'bootstrap-switch').click()

        with open(csv_output, 'w') as csv_file:
            # parse each page with the clients individually
            for i in range(100): # I've set 100 as a safety number in case the loop doesn't stop for some reason

                # selects every user and opens and then scraps their respective pages
                for user in driver.find_element(By.ID, "sortabletbl0").find_elements(By.CSS_SELECTOR, "tr")[1:]:
                    given_name = user.find_elements(By.CSS_SELECTOR, "td")[2].text
                    surname = user.find_elements(By.CSS_SELECTOR, "td")[3].text
                    email = user.find_elements(By.CSS_SELECTOR, "td")[5].text

                    # opens the page of the user in a new window
                    user.find_element(By.CSS_SELECTOR, "a").send_keys('\ue009' + '\ue007') # Control + Enter
                    
                    # goes to the user window, scrapes it and comes back
                    driver.switch_to.window(driver.window_handles[1])

                    # We need to give it a few seconds to load the page
                    while(len(driver.find_elements(By.ID, 'contentarea')) == 0):
                        time.sleep(0.5)
                    
                    # gets every service of an user
                    get_services(driver, csv_file, given_name, surname, email)
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                
                # while there is a link to go to the next page I click, otherwise I break to stop
                try:
                    driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page").click()
                except:
                    break
            
if __name__ == '__main__':
    main()
