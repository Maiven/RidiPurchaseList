# 리디북스 구매목록 추출

# RidiPurchaseList
Python scripts that parse the Ridibooks purchase list.

# Prerequisite
Python version: 3.7

Install BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/) and Selenium (http://selenium-python.readthedocs.io/)
- **$ pip install beautifulsoup4**
- **$ pip install selenium**

Get a Chromedriver for your OS in the following URL
- http://chromedriver.chromium.org/downloads
- Copy the executable to the same directory with scripts.

Locate your Chromedriver location in ridi_purchase_list.py
- on Windows, chrome_driver = './chromedriver.exe'
- on Mac or Linux, chrome_driver = './chromedriver'

# Run
- Locate to the directiory in command terminal. (windows: cmd / Mac: Terminal)
- **$ python ridi_purchase_list.py**
- Wait until the chrome window is appeared
- Login with your ridibooks account
- Wait. Tada! Your purchase list is saved in **purchase_list.csv**

