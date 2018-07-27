# -*- coding: utf-8 -*-

import csv
import urllib.request
from bs4 import BeautifulSoup

in_file = 'purchase_list.csv'
out_file = 'purchase_list_withISBN.csv'

numLine = sum(1 for line in open(in_file))

print('Number of Books:', numLine-1)

processed = 0

with open(out_file, 'wb') as unicode_file:
    unicode_file.write(b'\xef\xbb\xbf')

with open(in_file, 'r', encoding='utf-8') as incsv:
    with open(out_file, 'a', newline='', encoding='utf-8') as outcsv:
        reader = csv.reader(incsv)
        writer = csv.writer(outcsv, quoting=csv.QUOTE_MINIMAL)

        next(reader)
        for row in reader:
            url = 'https://ridibooks.com/v2/Detail?id=%d'%(int(row[0]))
            with urllib.request.urlopen(url) as f:
                html = f.read(8000)

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

            row.append(ISBN)
            writer.writerow(row)
            processed += 1
            print (processed,'/',numLine,'\t',','.join(row))