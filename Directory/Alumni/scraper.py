# Written by Luca Araújo, '26
# Fall, 2022

# Takes as input a csv file with output of WHMCS_Webscraper and fills in the role for the users that are listed in alumni directory
# Queries the alumni directory and if there is a match returns a csv with  the class year of the first person
# that matched, including the first and last name given and adding the role in the format (Alum - YEAR)

# Since the directory was quite tricky to navigate and it had sometimes super fast or super slow response times
# this code requires manual input to work. In the beginning the user needs to login to the alumni directory
# and then press enter every time, first to send in the first query after login and then to scrape the current one
# and send in the next query, it can only be pressed when the directory comes back with a response to the query

import csv
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service

# input
csv_input = 'unknown_data.csv'

csv_alumni = 'alumni.csv'
csv_non_carleton = 'non_carleton.csv'

non_carleton = []
alumni = []

def scrape(driver, row):
    try:
        row[3] = 'Alum - ' + \
            driver.find_element(By.CLASS_NAME, 'alumni-directory__cohort-year').text)
        alumni.append(row)
    except:
        non_carleton.append(row) # the person was not found in the directory

def write_array(csv_filename, array_out):
    with open(csv_filename, 'w') as csvfile:
        csvf = csv.writer(csvfile)
        for row in array_out:
            csvf.writerow(row)

def launch_browser():
    s=Service('./geckodriver')
    driver = webdriver.Firefox(service=s)
    return driver

def main():
    driver = launch_browser()
    driver.get('https://www.carleton.edu/alumni/directory/')
    driver.maximize_window()

    print("Login to the alumni directory and then press enter")
    a = input() # just wait for the user to login to then continue
    
    with open(csv_input, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            driver.find_element(By.ID, 'fullName').send_keys(row[0] + ' ' + row[1])

            driver.find_element(By.ID, 'campus-directory__submit').click()

            a = input()
            scrape(driver, row)

            driver.find_element(By.ID, 'fullName').clear()

    write_array(csv_alumni, alumni)
    write_array(csv_non_carleton, non_carleton)

    driver.close()
    driver.quit()

if __name__ == '__main__':
    main()
