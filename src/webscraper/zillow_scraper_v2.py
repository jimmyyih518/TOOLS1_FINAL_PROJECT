from urllib.parse import urlencode
import json
import httpx

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
        
        data = response.json()
        return data["cat1"]["searchResults"]["mapResults"]