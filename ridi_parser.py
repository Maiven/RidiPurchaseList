import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def checkExpire(bs_ele):
    rental = bs_ele.find(class_='rental_period')

    isRental = not(rental is None)

    expire = ''
    if isRental:
        period = rental.find(class_='period_time')
        expire = rental.find(class_='expired')
        isExpired = not(rental.find(class_='expired') is None)
        if isExpired:
            expire = 'END'
        else:
            expire_text = period.get_text().strip()
            day = re.search('([0-9]*)(일)', expire_text)
            hour = re.search('([0-9]*)(시간)', expire_text)

            expire = 0.0

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
    booklist = soup.find_all(id='book_')
    
    try:
        child = soup.find(class_='children_text')
        for tag in child.find_all('span'):
            tag.decompose()
        series = child.get_text().strip()
    except Exception:
        series = ''

    output = []

    for book in booklist:
        title = book.find(class_='title_text').get_text().strip()
        author = re.sub(' +', ' ', book.find(class_='author').get_text().strip())
        link = 'https://ridibooks.com'+book.find(class_='title_link')['href']
        thumbnail = book.find(class_='thumbnail')['src']
        expire = checkExpire(book)
        isGroup = not (book.find(class_='series_book') is None)
        
        if isGroup:
            book_id = 0
        else:
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

        output.append(bookinfo)

    soup.decompose()
    return output

def get_header_line():
    return ['ID', 'Title', 'Author', 'Group', 'GroupName', 'ExpireDate', 'Link']


def get_a_page(crawler, pageNum):
    crawler.get('https://ridibooks.com/library/?page=%d'%(pageNum))   
    html = crawler.page_source

    return parse_a_page(html)

def get_a_group_page(crawler, link, pageNum):
    url = urlparse(link)
    clean_link = '%s://%s%s?page=%d' % (url[0], url[1], url[2], pageNum)

    crawler.get(clean_link)
    html = crawler.page_source

    return parse_a_page(html)
    
# TEST ROUTINE
if __name__ == '__main__':
    import io

    with open('sample.html', 'r') as f:
        html = f.read()
        out = parse_a_page(html)

        for book in out:
            print(book)