# requests and flask framework
import requests
from flask import Flask
from flask import request

# nlp libs
import nltk
import re

# others
import pprint
from bs4 import BeautifulSoup
import json

# my modules
from strings import *
import queryprocessor
import responses
import gadata

app = Flask(__name__)

# function to fetch device information from GSMArena.com
def deviceInfo(phone, resolvedQuery):
#     I may need to replace spaces in the search string with + signs
    
    # perform a search for the phone and obtain search result page
    params = {
        GA_SEARCHURL_PARAM1: 'yes', 
        GA_SEARCHURL_PARAM2: phone
    }
    res = requests.get(GA_SEARCHURL, params)
    html_doc = res.text
    
    # parse the results page and look for phones
    soup = BeautifulSoup(html_doc, HTML_PARSER)
    if soup.find(class_="makers"): 
        rawSearchResults = soup.find(class_="makers").ul.find_all("li")
    else:         
        return responses.ApiAiResponse().dict
    
#     issue: some searches go directly to the device info page, invalidating the above html parsing: eg. nexus 6p
    
    searchResults = []    
    for rawSearchResult in rawSearchResults[:3]:
        searchResult = {}
        searchResult['link'] = GA_BASEURL + rawSearchResult.a.get('href')
        searchResult['image'] = rawSearchResult.img.get('src')
        searchResult['description'] = rawSearchResult.img.get('title')
        searchResult['name'] = re.sub(r'\<\/?br\>', ' ', ''.join(str(element) for element in rawSearchResult.a.span.contents)).strip()
        
        searchResults.append(searchResult)
    
    if searchResults: 
        topResult = searchResults[0]
    else: 
        return paramExtractor(resolvedQuery)
    
    # build api.ai response    
    speech = topResult['name'] + "\n\n" + topResult['description']
    displayText = topResult['name'] + "\n\n" + topResult['description']
    link = topResult['link']
        
    response = responses.ApiAiResponse()
    response.format(speech, displayText, link)
               
    return response.dict

def paramExtractor(resolved_query):
    
    qp = queryprocessor.QueryProcessor()
    
    resolved_query = qp.preprocess(resolved_query)
    return_text, noun_phrases = qp.extract_NPs(resolved_query)
    parameters = qp.extract_parameters(noun_phrases)

    parameters = pprint.pformat(parameters, 4)
    
    response = responses.ApiAiResponse()
    response.setSpeech(parameters)
    response.setDisplayText(parameters)
    return response.dict

@app.route('/webhook', methods=['POST'])
def handler():   
    reqBody = request.get_json()
    resolvedQuery = reqBody['result']['resolvedQuery']
    
    apiAiResponse = {}
    
    intentName = reqBody['result']['metadata']['intentName']
    if intentName == "deviceInfo":
        # get phone name
        phone = reqBody['result']['parameters']['phone']        
        apiAiResponse = deviceInfo(phone, resolvedQuery)
    
    else:                        
        apiAiResponse = paramExtractor(resolvedQuery)
                   
    # a response HAS to be sent
    return json.dumps(apiAiResponse)