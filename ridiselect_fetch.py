import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = './chromedriver'

pageStart = 1
pageEnd = 2

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
# driver = webdriver.Chrome(chrome_driver, chrome_options=options)
option = webdriver.ChromeOptions()
#option.add_argument('headless')
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(chrome_driver, chrome_options=option)
driver.implicitly_wait(5)

driver.get('https://ridibooks.com/account/login')
print("Please login to the Ridibooks page")

try:
    element = WebDriverWait(driver, 3600).until(
        EC.presence_of_element_located((By.ID, "divMyMenuLayer"))
    )
finally:
    print("Login detected")

filename = 'select_list.csv'

# Unicode header
with open(filename, 'wb') as unicode_file:
    unicode_file.write(b'\xef\xbb\xbf')

with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
    page = pageStart
    listwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

    while page <= pageEnd:
        #driver.get('https://select.ridibooks.com/books?page=%d'%(page))
        driver.get('https://select.ridibooks.com/new-releases?page=%d'%(page))
        elements = driver.find_elements_by_class_name('GridBookList_ItemLink')
        
        if len(elements) == 0:
            break

        print("Page:", page)
        links = []

        for elem in elements:
            link = elem.get_attribute('href')
            title = elem.find_element_by_class_name('GridBookList_ItemTitle').text
            bookid = link.split('/')[-1]
            
            links.append((link, bookid, title))

        for tup in links:
            link = tup[0]
            bookid = tup[1]
            title = tup[2]

            mainLink = 'https://ridibooks.com/v2/Detail?id=%s'%(bookid)

            # driver.get(link)
            # categoriy = driver.find_element_by_class_name('PageBookDetail_Categories').find_element_by_tag_name('span').text
            # author = driver.find_element_by_class_name('PageBookDetail_Authors').text
            # publisher = driver.find_element_by_class_name('PageBookDetail_Publisher').text[2:]

            driver.get(mainLink)

            try:
                category = driver.find_element_by_class_name('info_category_wrap').find_element_by_tag_name('a').text
            except Exception:
                category = ''

            author = ''

            try:
                authors = driver.find_element_by_class_name('author_item_wrapper').find_elements_by_tag_name('a')
            
                for elem in authors:
                    if author is '':
                        author = elem.text
                    else:
                        author += ', '+elem.text
            except Exception:
                author = ''
            

            try:
                publisher = driver.find_element_by_class_name('publisher_detail_link').text
            except Exception:
                publisher = ''

            try:
                subtitle = driver.find_element_by_class_name('info_title_sub_wrap').text
            except Exception:
                subtitle = ''

            output = [bookid, title, subtitle, author, publisher, category, link]
            print(output)
            # print('%s\t%s'%(bookid, title))
            listwriter.writerow(output)
            csvfile.flush() # whenever you want
        page += 1

    driver.close()

# with urllib.request.urlopen('https://select.ridibooks.com/books?page=%d'%(1)) as response:
#    html = response.read()
#    d = pq(html)

#    p = d('#RSGBookThumbnail_Link')
#    print(html)
   


