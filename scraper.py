import re
import bs4
import requests

import strings
import responses

class Scraper:
    """GSMArena.com web scraper"""
    
    ga_qs_url = strings.GA_QUICKSEARCH_URL
    ga_qs_param1 = strings.GA_QUICKSEARCH_URL_PARAM1
    ga_qs_param2 = strings.GA_QUICKSEARCH_URL_PARAM2
    ga_base_url = strings.GA_BASE_URL
    ga_pf_url = strings.GA_PHONEFINDER_URL
    html_parser_type = strings.HTML_PARSER
    
    def __fetch_page(self, url, http_get_params):
        """Perform a search for the given phone and obtain the search result page."""
                
        res = requests.get(url, http_get_params)
        print("HTTP GET %s" % res.url)
        html_doc = res.text
        return html_doc
    
    def __parse_page(self, html_doc):
        """Parse the results page and look for phones."""
        
        soup = bs4.BeautifulSoup(html_doc, Scraper.html_parser_type)
        if soup.find(class_="makers"): 
            raw_html_results = soup.find(class_="makers").ul.find_all("li")            
#         else:         
#             return vars(responses.ApiAiResponse())
        
        phones = []
        for result in raw_html_results[:3]:
            phone = {}
            phone['link'] = Scraper.ga_base_url + result.a.get('href')
            phone['image'] = result.img.get('src')
            phone['description'] = result.img.get('title')
            phone['name'] = re.sub(r'\<\/?br\>', ' ', ''.join(str(element) for element in result.a.span.contents)).strip()
            phones.append(phone)
        
        return phones
    
    def ga_quicksearch(self, phone):
        """Fetch device information from GSMArena.com using the regular search bar search."""
        
        print("Phone: %s" % phone)
        http_get_params = {Scraper.ga_qs_param1: 'yes', Scraper.ga_qs_param2: phone}
        html_doc = self.__fetch_page(Scraper.ga_qs_url, http_get_params)
        search_results = self.__parse_page(html_doc)
        return search_results
    
    def ga_phone_finder(self, parameters):
        """Use the parameters extracted from the user query to perform a search using GSMArena.com's phone finder feature."""
        
        http_get_params = parameters
        html_doc = self.__fetch_page(Scraper.ga_pf_url, http_get_params)
        search_results = self.__parse_page(html_doc)
        return search_results
         