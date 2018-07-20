import csv
from selenium import webdriver
from pyquery import PyQuery as pq
from urllib.parse import urlparse

chrome_driver = './chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('headless')

# driver = webdriver.Chrome(chrome_driver, chrome_options=options)
driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(3)

driver.get('https://ridibooks.com/account/login')
input("Please log in, and press Enter")

with open('result.csv', 'w', newline='') as csvfile:
    page = 50
    listwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

    while True:
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
   


