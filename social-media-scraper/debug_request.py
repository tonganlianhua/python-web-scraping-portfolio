#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug script to check weibo response"""

import requests

url = 'https://s.weibo.com/top/summary'
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get(url, headers=headers)
print(f'Status: {r.status_code}')
print(f'Length: {len(r.text)}')
print(f'Encoding: {r.encoding}')

# Save to file for inspection
with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

print('Saved to debug.html')

# Check for tbody
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
tbodies = soup.find_all('tbody')
print(f'Found {len(tbodies)} tbody elements')

for i, tbody in enumerate(tbodies):
    print(f'\nTbody {i}:')
    rows = tbody.find_all('tr')
    print(f'  Found {len(rows)} rows')
