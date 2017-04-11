# requests and flask framework
import requests
from flask import Flask
from flask import request

# nlp libs
# from stat_parser import Parser
import nltk
import re

# others
from pprint import pprint
from bs4 import BeautifulSoup
import json


app = Flask(__name__)

def deviceInfo(phone, resolvedQuery):
    # I may need to replace spaces in the search string with + signs
    
    payload = {'sQuickSearch': 'yes', 'sName': phone}
    res = requests.get('http://www.gsmarena.com/results.php3', params = payload)
#     print(res.url)
    html_doc = res.text
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    if soup.find(class_="makers"): rawSearchResults = soup.find(class_="makers").ul.find_all("li")
    else: return {"speech": "No results found.", "displayText": "No results found.", "data": {}, "source": "GSMArena"}
    
    # issue: some searches go directly to the device info page, invalidating the above html parsing: eg. nexus 6p
    
    searchResults = []    
    for rawSearchResult in rawSearchResults[:3]:
        searchResult = {}
        searchResult['link'] = "http://www.gsmarena.com/" + rawSearchResult.a.get('href')
        searchResult['image'] = rawSearchResult.img.get('src')
        searchResult['description'] = rawSearchResult.img.get('title')
        searchResult['name'] = re.sub(r'\<\/?br\>', ' ', ''.join(str(element) for element in rawSearchResult.a.span.contents)).strip()
        
        searchResults.append(searchResult)       
    
    if searchResults: topResult = searchResults[0]
#     else: return {"speech": "No results found.", "displayText": "No results found.", "data": {}, "source": "GSMArena"}
    else: return paramExtractor(resolvedQuery)
    
    # build api.ai response
    response = {}
    response['speech'] = topResult['name'] + "\n\n" + topResult['description']
    response['displayText'] = topResult['name'] + "\n\n" + topResult['description']
    response['data'] = {
        "facebook": {            
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": response['displayText'],
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": topResult['link'],
                            "title": "View Device Specs"
                        }
                    ]
                }
            }
        },
        "kik": {                        
            "type": "link", 
            "url": topResult['link'],
            "text": response['displayText']             
        },
#         "telegram": {
                            
#         }
    }
    
    response['contextOut'] = []
    response['source'] = "GSMArena"
        
    return response

def paramExtractor(resolvedQuery):     
    
    # convert things like 32GB to 32 GB
    resolvedQuery = re.sub(r"(\d+)\s*", r"\1 ", resolvedQuery)
    
    # NLTK POS tagging 
    posSentence = nltk.pos_tag(nltk.word_tokenize(resolvedQuery))
    print(posSentence)

    # NP-chunking using a tag pattern - refer to NLTK book chapter 7 for more details
    grammar = """        
        NP: {<DT>?<RB.*>*<CD>?<JJ.*>*<CD>?<NN.*>+}
        NP_P: {<NP>(<IN><NP>)+}
        
        SHOULD: {<MD><VB>}
        NP_S: {(<NP>|<PRP>)<SHOULD><IN><NP>}
        NP_J: {(<NP>|<PRP>)?<SHOULD><RB.*>*<CD>?<JJ.*>+<CD>?}
    """
    
#     NP_S captures phrases like, "the camera should be around 13 mp"
#     NP_J captures phrases like, "it should be pretty cheap"

#     NP: {<DT>?<RB.*>*<CD>?<JJ.*>*<CD>?<NN.*>+(<IN>?<CD>?<NN.*>*)+}
#     original rules:
#     NP: {(<DT>?<RB.*>*<JJ.*>*<CD>?<NN.*>+)}
#     PP: {<IN><NP>}
#     NP: {<NP><PP>}
    
    rp = nltk.RegexpParser(grammar)
    result = rp.parse(posSentence)    
    result.pprint()
    
    # extract noun phrases from tree
    NPTypes = ["NP", "NP_S", "NP_J", "NP_P"]
    returnText = ""
    nounPhrases = []
    for subtree in result.subtrees():
        if subtree.label() in NPTypes: 
            returnText += (str(subtree) + "\n\n")            
            nounPhrases.append(subtree)
    
#     for nounPhrase in reversed(nounPhrases):
#         print(nounPhrase.leaves())
        
#     print(nounPhrases)
    
    response = {"speech": returnText, "displayText": returnText, "data": {}, "contextOut": [], "source": "GSMArena"}
    return response    

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