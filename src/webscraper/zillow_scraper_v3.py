from urllib.parse import urlencode
import json
import httpx
from src.webscraper.zillow_scraper import ZillowScraper as v1_ZillowScraper
from src.webscraper.utils.scraper_utils import json_savefile
from tqdm import tqdm

v1_scraper = v1_ZillowScraper()

class ZillowScraper:
    def __init__(self):
        self.request_headers = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US;en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
        }
        
        self.url = "https://www.zillow.com/search/GetSearchPageState.htm?"
        self.base_url = 'https://www.zillow.com'
        
        
    def _build_query_url(self, **kwargs):
        # default to Vancouver, BC boundaries
        defaultKwargs = {'west_bound':-123.09948652478798, 
                         'east_bound':-122.69779890271766, 
                         'south_bound':49.157592000829325, 
                         'north_bound':49.34449321557116,
                         'search_term' : 'Vancouver, BC',}
        
        kwargs = {**defaultKwargs, **kwargs}
        
        parameters = {
            "searchQueryState": {
                "pagination": {},
                "usersSearchTerm": kwargs['search_term'],
                "mapBounds": {
                    "west": kwargs['west_bound'],
                    "east": kwargs['east_bound'],
                    "south": kwargs['south_bound'],
                    "north": kwargs['north_bound'],
                },
            },
            "wants": {
                # cat1 stands for agent listings
                "cat1": ["mapResults"]
                # and cat2 for non-agent listings
                # "cat2":["mapResults"]
            },
            "requestId": 2,
        }

        return self.url + urlencode(parameters)
    
    def scrape_listings(self, **kwargs):
        query_url = self._build_query_url(**kwargs)
        response = httpx.get(query_url, headers=self.request_headers)
        
        resp_raw = response.json()
        data = resp_raw["cat1"]["searchResults"]["mapResults"]
        
        if 'max_listings_limit' in kwargs:
            data = data[:kwargs['max_listings_limit']]
        
        data = self._get_additional_details(data)
        
        if 'savefile' in kwargs:
            json_savefile(data, kwargs['savefile'])
            
        return data
    
    def _get_additional_details(self, listings, v1_scraper = v1_scraper):
        error_count = 0
        for listing in tqdm(listings):
            try:
                url = self.base_url + listing['detailUrl']
                details = v1_scraper._query_single_detail(url)
                listing['additional_details'] = details
            except Exception as e:
                error_count += 1
                listing['additional_details'] = f'Error: {e}'
        
        print(f'{error_count}/{len(listings)} encountered error retrieving additional details')
        return listings