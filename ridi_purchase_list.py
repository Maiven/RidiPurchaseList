# -*- coding: utf-8 -*-

import csv
import ridi_parser as ridi
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = './chromedriver.exe'
### MAIN FUNCTION HERE
option = webdriver.ChromeOptions()
#option.add_argument('headless')
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(chrome_driver, chrome_options=option)
#driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(5)

driver.get('https://ridibooks.com/account/login')
print("Please login to the Ridibooks page")

try:
    while(not (driver.find_element_by_id('login_id') is None)):
        continue
except Exception:
    print("Successful login detected")

filename = 'purchase_list.csv'

# Unicode header
with open(filename, 'wb') as unicode_file:
    unicode_file.write(b'\xef\xbb\xbf')

with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
    page = 1
    listwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    listwriter.writerow(ridi.get_header_line())

    while True:
        books = ridi.get_a_page(driver, page)
        if len(books) == 0:
            break

        for book in books:
            if not book['isGroup']:
                print(book['title'])
                listwriter.writerow(book.values())
                csvfile.flush()
            else:
                subPage = 1
                while True:
                    group_books = ridi.get_a_group_page(driver, book['link'], subPage)
                    if len(group_books) == 0:
                        break
                    for group_book in group_books:
                        print((group_book['title']+' in '+group_book['series']))
                        group_book['isGroup'] = True
                        listwriter.writerow(group_book.values())
                        csvfile.flush()
                    subPage += 1
        page += 1

    driver.close()

