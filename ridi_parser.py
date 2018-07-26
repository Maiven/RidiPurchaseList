import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def checkExpire(bs_ele):
    rental = bs_ele.find(class_='LibraryBook_ExpireDate')
    isRental = not(rental is None)

    expire = ''
    if isRental:
        expire = 0.0

        expire_text = rental.get_text().strip()
        day = re.search('([0-9]*)(일)', expire_text)
        hour = re.search('([0-9]*)(시간)', expire_text)
        if not(day is None):
            expire += float(day[1])
        if not(hour is None):
            expire += float(hour[1])/24
                
    return expire

def get_id(address):
    o = re.search('(id=)([0-9]*)', address)
    return o[2]


def parse_a_page(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    booklist = soup.find_all(class_='LibraryBookList_Book')
    
    try:
        child = soup.find_all(class_='PageTitle_MainTitle')

        cnt = 0
        for elem in child:
            series = elem.get_text().strip()
            cnt+= 1
        if cnt == 1:
            series = ''
        
    except Exception:
        series = ''

    output = []

    for book in booklist:
    
        title = book.find(class_='RSGBookMetadata_Title').get_text().strip()
        try:
            author = re.sub(' +', ' ', book.find(class_='RSGBookMetadata_Authors').get_text().strip())
        except Exception:
            author = ''
        isGroup = not (book.find(class_='LibraryBook_UnitCount_Title') is None)
        #thumbnail = book.find(class_='RSGBookThumbnail_CoverImage')['src']
        expire = checkExpire(book)
        link = ''
        
        if isGroup:
            book_id = 0
        else:
            link = 'https://ridibooks.com'+book.find(class_='RSGBookMetadata_Title')['href']
            book_id = int(get_id(link))
            link = 'https://ridibooks.com/v2/Detail?id='+str(book_id)

        bookinfo = {
            'id':book_id,
            'title':title, 
            'author':author, 
            #'thumbnail':thumbnail, 
            'isGroup':isGroup, 
            'series':series,
            'expire':expire,
            'link':link}

        #print(bookinfo)
        output.append(bookinfo)

    soup.decompose()
    return output

def get_header_line():
    return ['BookID', u'도서명', u'저자', 'isSet', u'세트명', '대여만료', 'Link']


def get_a_page(crawler, pageNum):
    crawler.get('https://ridibooks.com/library/?order=purchase_date%%2Bdesc&filter=&page=%d'%(pageNum))   
    
    try:
        element = WebDriverWait(crawler, 3600).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LibraryBookList"))
        )
    finally:
        html = crawler.page_source
    
    return parse_a_page(html)

def get_a_group_link(crawler, pageNum, groupNo):
    crawler.get('https://ridibooks.com/library/?order=purchase_date%%2Bdesc&filter=&page=%d'%(pageNum))   
    
    try:
        element = WebDriverWait(crawler, 3600).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LibraryBookList"))
        )
    finally:
        subs = crawler.find_elements_by_class_name("LibraryBook_UnitCount_Title");

    itemno = 0
    for group in subs:
        itemno+= 1
        if (itemno != groupNo):
            continue;
        group.click()
        break

    link = crawler.current_url

    return link


def get_a_group_page(crawler, link, pageNum):
    url = urlparse(link)
    clean_link = '%s://%s%s?order=unit_order%%2Basc&page=%d' % (url[0], url[1], url[2], pageNum)

    crawler.get(clean_link)

    try:
        element = WebDriverWait(crawler, 3600).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LibraryBookList"))
        )
    finally:
        html = crawler.page_source

    return parse_a_page(html)
    
# TEST ROUTINE
if __name__ == '__main__':
    import io

    with open('list_sample.html', 'r') as f:
        html = f.read()
        out = parse_a_page(html)

        for book in out:
            print(book)
