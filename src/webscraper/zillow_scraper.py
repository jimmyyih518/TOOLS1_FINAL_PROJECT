from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
import re
import os
from urllib3.exceptions import InsecureRequestWarning
from .utils.scraper_utils import json_savefile, hash_json


class ZillowScraper:
    def __init__(self):
        self.query_listing_headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                'Accept-Encoding': 'identity'
                }
        
        self.query_detail_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.temp_listing_data = []   
        self.temp_details_data = []
    
    def scrape(self, city,max_price,min_beds,min_baths,min_homesize,min_lotsize, savefile=None):
        all_listings = self._query_listings(city,max_price,min_beds,min_baths,min_homesize,min_lotsize)
        for listing in all_listings['query_result']:
            listing_url = listing['url']
            print(listing)
            listing['scraped_data'] = self._query_single_detail(listing_url)
            
        if savefile:
            json_savefile(all_listings, savefile)
            
        return all_listings

    def _query_listings(self, city,max_price,min_beds,min_baths,min_homesize,min_lotsize, savefile=None):

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
            max%22%3A{max_price}%7D%2C%22
            beds%22%3A%7B%22
            min%22%3A{min_beds}%7D%2C%22
            baths%22%3A%7B%22
            min%22%3A{min_baths}%7D%2C%22
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
            min%22%3A{min_homesize}%7D%2C%22
            lot%22%3A%7B%22
            min%22%3A{min_lotsize}%7D%7D%2C%22
            isListVisible%22%3Atrue%2C%22
            mapZoom%22%3A12%7D
            '''
            
        url="".join([x.strip() for x in url.splitlines()])
        print(url)
        query_string = urllib.parse.urlsplit(url).query
        params = urllib.parse.parse_qs(query_string)
        print(params)
        response=requests.get(url,headers=self.query_listing_headers)
        
        if response.status_code != 200:
            return response
    
        print(response)
        # fetch HTML content
        html_content = response.text
        tempfile = dict(params)
        tempfile['html_content'] = html_content
        tempfile['url'] = url
        self.temp_listing_data.append({query_string:tempfile})
        # parse the content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')
    
        # extract all listings
        script_text = soup.find_all('script', type='application/ld+json')
        alldata = []
        for t in script_text:
            data = json.loads(t.text)
            #print(data)
            alldata.append(data)
            
        result = {
            'query_result':[x for x in alldata if len(x) == 7], 
            'query_params':params
            }
        
        if savefile:
            json_savefile(result, savefile)
                
        return result
    
    
    def _query_single_detail(self, url, savefile=None):
        
        req_result = requests.get(url, headers=self.query_detail_headers)
        req_text = req_result.text
        req_soup = BeautifulSoup(req_text, 'lxml')
        summary_data = req_soup.find_all('div', class_='summary-container')
        summary_text = summary_data[0].text
        details_data = req_soup.find_all('div', class_='ds-data-view-list')
        details_text = details_data[0].text
        
        result = {'summary':summary_text, 'details':details_text}
        
        if savefile:
            json_savefile(result, savefile)
        
        return result

