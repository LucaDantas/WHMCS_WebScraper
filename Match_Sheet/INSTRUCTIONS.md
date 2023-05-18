# WHMCS / WHM Scraper and Match Sheet Creator

## Author
Luca Araújo '2026, Written in March, 2023
For: Em Palencia

## How to run the program
### 1. Make sure you have Python and firefox on your machine, code was written on a linux machine but probably also runs in a MacOS system. Windows has not been tested but might work with minor changes.

### 2. Install the two LIBRARIES below by executing the two commands on the terminal
 `pip3 install selenium`\
 `pip3 install requests`\

### 3. Download this repository
Make sure you have a folder named `ScrapingCode` containing the files named:
`clients_data.py`\
`domains_data.py`\
`subdomains_data.py`\
`websites_data.py`\
`geckodriver`\

Make sure you have an empty folder named `raw` and an empty folder named `data`. The folder raw will be where the output of the scraping codes will be and the folder data will be where the output of pre-processed data will be.

Make sure there is a file named `process_data.py` and a file named `pre_process_raw_data.py`. The first one is the one that gets the data in the correct format form the `data` folder and creates the match sheet. The file `pre_process_data.py` takes the raw data and puts it into the correct format.

### 4. WEB DRIVER
If the driver (geckodriver) available on the folder doesn't work you might have to follow the following steps to update the driver to match your Firefox version. Check your firefox version version and download the matching driver here and then replace it with the one in the ScrapingCode folder, the provided driver is for linux so you will need to download the one for you operating system on the link below.

Geckdriver: https://github.com/mozilla/geckodriver/releases

### 5. Create CONFIG.PY to access WHM and WHMCS
Create files called `config_whmcs.py` and `config_whm.py` and add them to the ScrapingCode folder. This will contain log in information for WHMCS and for WHM respectively. You can copy-paste the format below into the files, and replace your_username and your_password with your credentials, please keep the quotation marks `''`.
```
username = 'your_username'
password = 'your password'
```

### 6. Run the program

Navigate to the ScrapingCope folder on your terminal. Run all the `_data.py` files on the folder to scrape the information from WHM and WHMCS.
If it doesn't work come back to the previous instructions and make sure that you have an updated firefox and its respective geckodriver and also that you have the correct login credentials on the respective config_whmcs.py and config_whm.py

After all the code ran the raw data should be on the raw folder (which is not a subfolder of ScrapingCode, it is inside the main folder).

Then come back to the main folder and run the `pre_process_raw_data.py`, it will take the information from the `raw` folder and put it into the correct format in the `data` folder.

Then run the `process_data.py` file and it will create the file `match_sheet.csv` and the `not_matched.csv` files which are the desired sheets.

