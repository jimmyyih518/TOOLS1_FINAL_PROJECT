from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
import pandas
import numpy
import matplotlib

def get_listings(city,maxprice,beds,baths,homesize,lotsize):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    url=f'''https://www.zillow.com/{city}-bc/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22     
        usersSearchTerm%22%3A%22{city}%2C%20BC%22%2C%22
        mapBounds%22%3A%7B%22
        west%22%3A-123.09948652478798%2C%22
        east%22%3A-122.69779890271766%2C%22
        south%22%3A49.157592000829325%2C%22
        north%22%3A49.34449321557116%7D%2C%22
        isMapVisible%22%3Atrue%2C%22
        filterState%22%3A%7B%22
        price%22%3A%7B%22
        min%22%3A0%2C%22
        max%22%3A{maxprice}%7D%2C%22
        beds%22%3A%7B%22
        min%22%3A{beds}%7D%2C%22
        baths%22%3A%7B%22
        min%22%3A{baths}%7D%2C%22
        mp%22%3A%7B%22
        min%22%3A0%2C%22
        max%22%3A9642%7D%2C%22
        ah%22%3A%7B%22
        value%22%3Atrue%7D%2C%22
        sort%22%3A%7B%22
        value%22%3A%22days%22%7D%2C%22
        tow%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        con%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        land%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        apa%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        manu%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        apco%22%3A%7B%22
        value%22%3Afalse%7D%2C%22
        sqft%22%3A%7B%22
        min%22%3A{homesize}%7D%2C%22
        lot%22%3A%7B%22
        min%22%3A{lotsize}%7D%7D%2C%22
        isListVisible%22%3Atrue%2C%22
        mapZoom%22%3A12%7D
        '''
    url="".join([x.strip() for x in url.splitlines()])
    print(url)
    query_string = urllib.parse.urlsplit(url).query
    params = urllib.parse.parse_qs(query_string)
    print(params)
    response=requests.get(url,headers=headers)
    if response.status_code != 200:
        return response

    print(response)
    # fetch HTML content
    html_content = response.text

    # parse the content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # extract all listings
    script_text = soup.find_all('script', type='application/ld+json')
    alldata = []
    for t in script_text:
        data = json.loads(t.text)
        #print(data)
        alldata.append(data)
        
    return [x for x in alldata if len(x) == 7]
    #return alldata

l1 = get_listings(city='Burnaby',maxprice=5000000,beds=4,baths=4,homesize=2000,lotsize=4000)

import json
with open('listing_data.json', 'w') as f:
    json.dump(l1, f, indent=4)

u1 = l1[0]['url']
u1 = 'https://www.zillow.com/homedetails/7515-Cascade-St-Burnaby-BC-V3N-4W1/314494424_zpid/'
import re
import os
from urllib3.exceptions import InsecureRequestWarning

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
r = requests.get(u1, headers=headers)
h = r.text
s = BeautifulSoup(h, 'lxml')
t1 = s.find_all('div', class_='summary-container')
a1 = t1[0].text
t2 = s.find_all('div', class_='ds-data-view-list')
a2 = t2[0].text
with open('single_listing_description.txt', 'w') as f:
    f.write(a2)

test = 'AbcdEfgh'

def split_caps(text):
    return re.findall('[A-Z][^A-Z]*', text)

split_caps(test)

a2a = [x for x in a2.split(' ')]

string = 'TypeSingle Family home BEDROOMS 6Bathrooms 4'

result = re.sub(r'^\s+([a-zA-Z]+)\s+([A-Z][a-z]+)', r' \1 \2', string)
result = [re.sub(r'\s+([a-zA-Z]+)\s+([a-zA-Z]+)', r'\1 \2', x) for x in a2a]

a2 = t2[0].text
data_dict = {}
import re
# Create output dictionary 
output_dict = dict() 
type_search = re.search(r'Type(.*)Year', a2) 
if type_search: 
    output_dict["Type"] = str(type_search.group(1)) 
d2 = parse_text(a2)
