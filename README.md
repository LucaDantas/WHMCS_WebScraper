# WHMCS_WebScraper
This code is to get WHMCS information.

## Author
Luca Araújo '2026, Written in September 29, 2022  
For: Em Palencia


## Summary
When scraper.py is run, it will sign into Carleton Colleges WHMCS page and scrape domain information and put it into a csv file for easy viewing.

## How to run the program
### 1. Make sure you have Python on your machine

### 2. Install the two LIBRARIES below by executing the two commands
 `pip3 install selenium`\
 `pip3 install requests`\
 `pip3 install bs4`\

### 3. Download this repo (Code > Download ZIP)

### 4. WEB DRIVER
You need to find the webdriver that matches your Chrome version. Check your chrome version and download the matching Chrome driver here.

Web drivers: https://chromedriver.storage.googleapis.com/index.html 

Replace the webdriver in this folder with the webdriver you just downloaded. 

You can also use Firefox. Follow the guidelines especified in the code commenting and uncommenting the specific lines and it will work.

Download the webdriver geckodriver that matches you firefox version and add it to this folder

Geckdriver: https://github.com/mozilla/geckodriver/releases

### 5. Create CONFIG.PY
create a file called `config.py`. This will contain log in information for WHMCS. You can copy-paste the format below into config.py, and replace your_username and your_password with the actual thing, please keep the `''`.
```
username = 'your_username'
password = 'your password'
```

### 6. Run the program
Navigate your command/terminal to the folder where you have the code. Use the following command the run the program. 
```
python3 scraper.py
```

