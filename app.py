# requests and flask framework
import requests
from flask import Flask
from flask import request

# nlp libs
import nltk
import re

# others
from pprint import pprint
from bs4 import BeautifulSoup
import json

# my modules
import responses
import gadata

app = Flask(__name__)

GA_BASEURL = 'http://www.gsmarena.com/'
GA_SEARCHURL = 'http://www.gsmarena.com/results.php3'
GA_SEARCHURL_PARAM1 = 'sQuickSearch'
GA_SEARCHURL_PARAM2 = 'sName'
HTML_PARSER = 'html.parser'

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

def paramExtractor(resolvedQuery):
    
    ### query preprocessing and clever hacks
    ########################################
    
    # convert \" to inch - 5" becomes 5inch
    resolvedQuery = re.sub(r"\"", r"inch", resolvedQuery)
    
    # convert things like 32GB to 32 GB - so that 32 is considered as CD and GB as NN/NNP
    resolvedQuery = re.sub(r"(\d+(.\d+)?)\s*", r"\1 ", resolvedQuery)
    
    # convert i to I so that we reduce the number of noun phrases captured
    resolvedQuery = re.sub(r"\bi\b", r"I", resolvedQuery)
    
    # convert GB to MB
    
    ### query processing
    ####################
    
    # NLTK POS tagging
    posSentence = nltk.pos_tag(nltk.word_tokenize(resolvedQuery))
#     print(posSentence)

    # NP-chunking using a tag pattern - refer to NLTK book chapter 7 for more details
    # NP_S captures phrases like, "the camera should be around 13 mp"
    # NP_J captures phrases like, "it should be cheap"
    grammar = """        
        NP: {<DT>?<RB.*>*<CD>?<JJ.*>*<CD>?<NN.*>+}
        NP_C: {<NP><NP>}
        NP_P: {<NP>(<IN><NP>)+}
        
        SHOULD: {<MD><VB>}
        NP_S: {(<NP>|<PRP>)<SHOULD><IN><NP>}
        NP_J: {(<NP>|<PRP>)?<SHOULD><RB.*>*<CD>?<JJ.*>+<CD>?}
    """
    
    rp = nltk.RegexpParser(grammar)
    result = rp.parse(posSentence)
#     result.pprint()    
    
    # extract noun phrases from tree
    NPTypes = ["NP", "NP_S", "NP_J", "NP_P", "NP_C"]
    returnText = ""
    nounPhrases = []
    for subtree in result.subtrees():
        if subtree.label() in NPTypes:
            returnText += (str(subtree) + "\n\n")
            nounPhrases.append(subtree)        
    
    params = gadata.parameters
    for nounPhrase in nounPhrases:
        np = nounPhrase.leaves()
        tokens = [tup[0].lower() for tup in np]
        phrase = ' '.join(tokens)
        bigrams = [' '.join(tuple) for tuple in list(nltk.bigrams(tokens))]
        tags = [tup[1] for tup in np]
        
        for param in params:
            if param['category'] == 'value':
                for id in param['identifiers']:
                    if id in tokens or id in bigrams:
                        if param['type'] == 'csv':
                            print param['reference'] + ' = ' + str(param['values'][id])
                        elif param['type'] == 'radio':
                            print param['reference'] + ' = ' + str(param['values']['yes'])
                        elif param['type'] == 'check':
                            print param['reference']            
                        
            elif param['category'] == 'general':
                for id in param['reference_identifiers']:
                    if id in tokens or id in bigrams:
                        if 'pattern' in param:
                            regex = param['pattern']
                            match = re.search(regex, phrase)
                            if match:
                                print param['reference'] + ' = ' + match.group(0)
                                break                                                                           
                            
                        if 'pos' in param:
                            # if pos in tags
                            for pos in param['pos']:
                                if pos in tags:
                                    lingvar = tokens[tags.index(pos)]
                                    print param['reference'] + ' = ' + lingvar
#                             break
                        
                        if 'values' in param:
                            if param['type'] == 'radio':
                                print param['reference'] + ' = ' + str(param['values']['yes'])
                            else:
                                for val in param['values']:
                                    if val in tokens:
                                        print param['reference'] + ' = ' + str(param['values'][val])
                                        break
        print tokens
        print tags
        print
    
    response = responses.ApiAiResponse()
    response.setSpeech(returnText)
    response.setDisplayText(returnText)
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