import re
import bs4
import requests

import strings
import responses
import queryprocessor

class Scraper:
    """GSMArena.com web scraper"""
    
    qs_url = strings.GA_QUICKSEARCH_URL
    qs_param1 = strings.GA_QUICKSEARCH_URL_PARAM1
    qs_param2 = strings.GA_QUICKSEARCH_URL_PARAM2
    html_parser_type = strings.HTML_PARSER    
    ga_base_url = strings.GA_BASEURL
    
    def _fetch_page(self, phone):
        """Perform a search for the given phone and obtain the search result page."""
        
        params = {Scraper.qs_param1: 'yes', Scraper.qs_param2: phone}
        res = requests.get(Scraper.qs_url, params)
        html_doc = res.text
        return html_doc
    
    def _parse_page(self, html_doc):
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
        else:
            qp = queryprocessor.QueryProcessor()            
            parameters = qp.process(query)
            return parameters
        
        # build api.ai response
        speech = topResult['name'] + "\n\n" + topResult['description']
        displayText = topResult['name'] + "\n\n" + topResult['description']
        link = topResult['link']
        
        response = responses.ApiAiResponse()
        response.format_device_info(speech, displayText, link)
        return vars(response)
    
    def quicksearch(self, phone, query):
        """Fetch device information from GSMArena.com."""
                
        html_doc = self._fetch_page(phone)
        search_results = self._parse_page(html_doc)           
        return search_results