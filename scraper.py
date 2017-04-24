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
        print res.url
        html_doc = res.text
        return html_doc
    
    def __parse_page(self, html_doc):
        """Parse the results page and look for phones."""
        
        soup = bs4.BeautifulSoup(html_doc, Scraper.html_parser_type)
        if soup.find(class_="makers"): 
            rawSearchResults = soup.find(class_="makers").ul.find_all("li")            
        else:         
            return vars(responses.ApiAiResponse())
        
        #     issue: some searches go directly to the device info page, invalidating the above html parsing: eg. nexus 6p
        
        searchResults = []
        for rawSearchResult in rawSearchResults[:3]:
            searchResult = {}
            searchResult['link'] = Scraper.ga_base_url + rawSearchResult.a.get('href')
            searchResult['image'] = rawSearchResult.img.get('src')
            searchResult['description'] = rawSearchResult.img.get('title')
            searchResult['name'] = re.sub(r'\<\/?br\>', ' ', ''.join(str(element) for element in rawSearchResult.a.span.contents)).strip()

            searchResults.append(searchResult)

        if searchResults:
            topResult = searchResults[0]
        
        # build api.ai response
        speech = topResult['name'] + "\n\n" + topResult['description']
        displayText = topResult['name'] + "\n\n" + topResult['description']
        link = topResult['link']
        
        response = responses.ApiAiResponse()
        response.format_device_info(speech, displayText, link)
        return vars(response)
    
    def ga_quicksearch(self, phone):
        """Fetch device information from GSMArena.com using the regular search bar search."""
        
        http_get_params = {Scraper.ga_qs_param1: 'yes', Scraper.ga_qs_param2: phone}
        html_doc = self.__fetch_page(Scraper.ga_qs_url, http_get_params)
        search_results = self.__parse_page(html_doc)
        return search_results
    
    def ga_phone_finder(self, parameters):
        """Use the parameters extracted from the user query to perform a search using GSMArena.com's phone finder feature."""
        
        html_doc = self.__fetch_page(Scraper.ga_pf_url, parameters)
        search_results = self.__parse_page(html_doc)
        return search_results