# Written by Luca Araújo, '26
# Fall, 2022

# Does not use beautiful soup, only selenium

# Get the users scraped roles and write them to WHMCS admin notes
# If someone already has a role written on WHMCS admin notes it doesn't do anything to avoid repetition, prints them to the screen only

import config
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

csv_data = '../Data_Processed/data_processed.csv'

email_to_roles = {}

def write_notes(driver):
    text_box = driver.find_element(By.CSS_SELECTOR, 'textarea')
    email = driver.find_element(By.CLASS_NAME, 'clientssummarystats').find_elements(By.CSS_SELECTOR, 'tr')[3].find_elements(By.CSS_SELECTOR, 'td')[1].text

    if email in email_to_roles:
        print(email, email_to_roles[email])
        if text_box.text != email_to_roles[email]:
            if text_box.text == '':
                text_box.send_keys(email_to_roles[email])
            else:
                print(f"The user {email}  already has something written")
                # text_box.send_keys(" | " + email_to_roles[email])
            time.sleep(2)
            driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div/div[1]/div[2]/div[4]/div[3]/form/div/input').click()
    else:
        print("cannot find email")

# lauches the webdriver.
# if you want to use firefox uncomment the first two lines and comment the respective lines for chrome
def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def read_csv():
    global csv_data
    with open(csv_data, 'r') as csvfile:
        reader = csv.reader(csvfile);
        for row in reader:
            email_to_roles[row[2]] = row[3]

def main():
    read_csv()

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
                time.sleep(3)
                
                write_notes(driver)

                time.sleep(1)
                
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
