# Adds students on WHMCS to WHMCS groups based on their class year
# Needs to have that information written on WHMCS's admin notes

import config
import csv
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

id_grp = {'2023' : 1, '2024' : 5, '2025' : 6, '2026' : 7}

def add_to_group(driver):
    while(len(driver.find_elements(By.CSS_SELECTOR, 'textarea')) == 0):
        time.sleep(0.5)
    text_box = driver.find_element(By.CSS_SELECTOR, 'textarea')
    user_id = int(driver.find_element(By.CSS_SELECTOR, '#userId').text)
    email = driver.find_element(By.CLASS_NAME, 'clientssummarystats').find_elements(By.CSS_SELECTOR, 'tr')[3].find_elements(By.CSS_SELECTOR, 'td')[1].text
    role = text_box.text
    print(email, role)

    if role == "":
        print("vazio")
        return

    if 'Student' not in role:
        print('This person is not of a role we want to categorize')
        return
    
    print("Found a matching user")
    driver.find_element(By.ID, 'clientTab-2').click()

    while(len(driver.find_elements(By.XPATH, '/html/body/div[8]/div[1]/div/div/form/table/tbody/tr[14]/td[4]/select')) == 0):
        time.sleep(1)

    choose_group = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/form/table/tbody/tr[14]/td[4]/select')
    for year in ['2023', '2024', '2025', '2026']:
        if year in role:
            choose_group.find_element(By.CSS_SELECTOR, f'[value="{id_grp[year]}"]').click()
            print(f'Added user to Student - {year} group')

    driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/form/div/input[1]').click()
    print("User group assignment confirmed")


def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    # launches browser
    with launch_browser() as driver:
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

            time.sleep(3)

            # selects every user and opens and then scraps their respective pages
            for user in driver.find_element(By.ID, "sortabletbl0").find_elements(By.CSS_SELECTOR, "tr")[1:]:
                # opens the page of the user in a new window
                user.find_element(By.CSS_SELECTOR, "a").send_keys('\ue009' + '\ue007') # Control + Enter
     
                # goes to the user window, scrapes it and comes back
                driver.switch_to.window(driver.window_handles[1])

                add_to_group(driver)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            # while there is a link to go to the next page I click, otherwise I break to stop
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page").click()
            except:
                break

if __name__ == '__main__':
    main()
