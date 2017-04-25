import flask

import queryprocessor
import responses
import strings
import scraper
import gadata

# initialize stuff
app = flask.Flask(__name__)
sc = scraper.Scraper()
qp = queryprocessor.QueryProcessor()
api_ai_response = {}

@app.route('/webhook', methods=['POST'])
def handler():   
    req_body = flask.request.get_json()    
    query = req_body['result']['resolvedQuery']
    phone = req_body['result']['parameters']['phone'] if 'phone' in req_body['result']['parameters'] else ''
    intent = req_body['result']['metadata']['intentName']
            
    if intent == strings.DEVICEINFO_INTENT:
        api_ai_response = sc.ga_quicksearch(phone)
        
    elif intent == strings.SEARCHPHONE_INTENT or intent == strings.FALLBACK_INTENT:        
        api_ai_response = qp.process(query)        
    
    else:
        api_ai_response = responses.ApiAiResponse().get()
        
    return api_ai_response