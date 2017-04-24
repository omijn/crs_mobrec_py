# core
import pprint
import json

# flask framework
from flask import request
from flask import Flask

# my modules
import queryprocessor
import responses
import strings
import scraper
import gadata

# initialize stuff
app = Flask(__name__)
sc = scraper.Scraper()
qp = queryprocessor.QueryProcessor()

@app.route('/webhook', methods=['POST'])
def handler():   
    req_body = request.get_json()    
    query = req_body['result']['resolvedQuery']
    phone = req_body['result']['parameters']['phone'] if 'phone' in req_body['result']['parameters'] else ''
    intent = req_body['result']['metadata']['intentName']
    
    api_ai_response = {}        
    
    if intent == strings.DEVICEINFO_INTENT:
        api_ai_response = sc.ga_quicksearch(phone)
    
    elif intent == strings.SEARCHPHONE_INTENT or intent == strings.FALLBACK_INTENT:
#         parameters = qp.process(query)
#         parameters = pprint.pformat(parameters, 4)

#         response = responses.ApiAiResponse()
#         response.set_speech(parameters)
#         response.set_display_text(parameters)

#         api_ai_response = vars(response)
        
        api_ai_response = qp.process(query)
                       
    return json.dumps(api_ai_response)