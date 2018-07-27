# -*- coding: utf-8 -*-

import csv
import urllib.request

from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_isbn(ridi_id):
    url = 'https://ridibooks.com/v2/Detail?id=%d'%(ridi_id)

    try:        
        with urllib.request.urlopen(url) as f:
            html = f.read()
    except Exception:
        html = ''

    soup = BeautifulSoup(html, 'html.parser')
    meta = soup.find_all('meta')

    ISBN = ''
    for elem in meta:
        try:
            prop = elem['property']
            if (prop == 'books:isbn'):
                ISBN = str(elem['content'])
                break
        except Exception:
            continue

    try:
        title = soup.find('h3', class_='info_title_wrap').text    
    except Exception:
        title = ''

    print(url,'\t==>',ISBN,'\t',title)

    return ISBN


def process_isbns():
    in_file = 'purchase_list.csv'
    out_file = 'purchase_list_withISBN.csv'
    numLine = sum(1 for line in open(in_file)) -1
    print('Number of Books:', numLine)

    ids = []
    with open(in_file, 'r', encoding='utf-8') as incsv:
        reader = csv.reader(incsv)
        next(reader)

        for row in reader:
            ids.append(int(row[0]))

    pool = Pool(processes = 8)
    ISBNs = pool.map(get_isbn, ids)
    
    with open(out_file, 'wb') as unicode_file:
        unicode_file.write(b'\xef\xbb\xbf')
    with open(in_file, 'r', encoding='utf-8') as incsv:
        with open(out_file, 'a', newline='', encoding='utf-8') as outcsv:
            reader = csv.reader(incsv)
            writer = csv.writer(outcsv, quoting=csv.QUOTE_MINIMAL)

            next(reader)
            cnt = 0
            for row in reader:
                ISBN = ISBNs[cnt]
                row.append(ISBN)
                writer.writerow(row)
               
                print (', '.join(row))
                cnt += 1



if __name__ == '__main__':
    process_isbns()
