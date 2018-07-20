import csv
import ridi_parser as ridi
from selenium import webdriver


chrome_driver = './chromedriver'
### MAIN FUNCTION HERE
option = webdriver.ChromeOptions()
#option.add_argument('headless')
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(chrome_driver, chrome_options=option)
#driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(3)

driver.get('https://ridibooks.com/account/login')
input("Please log in, and press Enter")

with open('purchase_list.csv', 'w', newline='') as csvfile:
    page = 1
    listwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

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
                        print(group_book['title'],'in',group_book['series'])
                        group_book['isGroup'] = True
                        listwriter.writerow(group_book.values())
                        csvfile.flush()
                    subPage += 1
        page += 1

    driver.close()

